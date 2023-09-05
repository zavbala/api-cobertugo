import json

import httpx
from fastapi import APIRouter, HTTPException
from lxml.etree import _Element
from pydantic import BaseModel
from typing import Optional
from zeep import Client
from zeep.wsse.username import UsernameToken
from glom import glom

from app.resources import strings, utils

with open("data/Tree.json", "r") as file:
    plain = file.read()
    data = json.loads(plain)

router = APIRouter()


class ProviderData(BaseModel):
    year: int
    brand: str
    model: str
    provider: str
    slug: Optional[str]


@router.post("")
async def get_models(body: ProviderData):
    providers = data.keys()
    dict_body = body.model_dump()
    file_name = body.provider.upper()

    if body.provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {file_name} not found")

    provider = data[body.provider]
    endpoints = provider["endpoints"]

    try:
        protocol = provider["protocol"]
    except KeyError:
        protocol = "SOAP"

    elements, output = [], []
    action, credentials = None, None

    # Calculate brand ID from provider
    if provider != "ANA":
        dict_body["brand"] = utils.resolve_brand(body.brand, body.provider)

    if protocol == "REST":
        action = endpoints["versions"]
        URL = provider["URL"] + action["path"]

        if "authentication" in provider:
            credentials = f"Bearer {provider['token']}"

        payload = utils.resolve_my_keys(action["schema"], **dict_body)

        response = httpx.get(
            URL,
            params=payload,
            headers={
                "Authorization": credentials,
                "Content-Type": strings.CONTENT_TYPE_JSON,
            },
        )

        entry = action["entry"]
        elements = response.json()[entry]

        if "struct" in action:
            struct = action["struct"]
            elements = [glom(item, struct) for item in elements]

    if protocol == "SOAP":
        is_xml = False

        if "authentication" in provider:
            credentials = list(provider["authentication"].values())

        # Provider needs compute ...
        if "brands" in endpoints:
            action = endpoints["brands"]
            payload = utils.resolve_my_keys(action["input"], **dict_body)

            URL = action["URL"] + "?WSDL"

            client = Client(
                URL, wsse=UsernameToken(*credentials) if credentials else None
            )

            get_brands = client.service[action["method"]](**payload)
            deserialized = utils.zeep_to_dict(get_brands, "subMarcaAuto")

            for child in deserialized:
                if child["descripcion"] == body.slug:
                    dict_body["subbrand"] = child["claveSubMarcaAuto"]

        action = endpoints["versions"]
        method = action["method"]

        if "URL" in provider:
            base = provider["URL"]
        else:
            base = action["URL"]

        URL = base + "?WSDL"
        client = Client(URL, wsse=UsernameToken(*credentials) if credentials else None)
        keys = utils.resolve_my_keys(action["input"], **dict_body)

        base_payload = provider["constants"] if "constants" in provider else {}
        payload = {**keys, **base_payload}
        response = client.service[method](**payload)

        if type(response) == str or isinstance(response, _Element):
            is_xml = True

            if type(response) == str:
                response = response.split("?>", 1)[1]

            response = utils.zeep_to_bs4(response)

        else:
            elements = utils.zeep_to_dict(response, action["entry"] or None)

            if "struct" in action:
                struct = action["struct"]
                elements = [glom(item, struct) for item in elements]

        # print(response)
        # return "ALV"

        # if is_xml:

        #     for item in response.find_all(action["entry"]):

        #         # zurich
        #         computed = {
        #                 "id": item["clave"],
        #                 "version": item.text.strip(),
        #             }

        #         elements.append(computed)

        if is_xml:
            for item in response.find_all(action["entry"]):
                print(item)
                computed = {
                    "id": item.select_one("ctarifa").text.strip(),
                    "version": item.select_one("cversion").text.strip(),
                }

                elements.append(computed)

    if "filter" in action:
        _filter_ = action["filter"]

        # Filter by pipe, check if model match into description
        if _filter_["type"] == "PIPE":
            for item in elements:
                if item["version"].split(" ").count(body.slug) > 0:
                    output.append(item)

        # Filter by equal, check if model is equal to value
        if _filter_["type"] == "EQUAL":
            for item in elements:
                if item[_filter_["by"]] == body.slug:
                    output.append(item)

        elements = output

    return {
        "year": body.year,
        "model": body.model,
        "brand": body.brand,
        "provider": body.provider,
        "slug": body.slug,
        "data": elements,
    }
