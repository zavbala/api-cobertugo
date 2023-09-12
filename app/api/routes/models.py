import json
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from glom import glom
from lxml import etree
from lxml.etree import _Element
from pydantic import BaseModel
from zeep import Client
from zeep.wsse.username import UsernameToken

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

    if provider != "ANA":
        provider_uses_long_brand = ["QUALITAS"].count(body.provider)

        id, brand_name = utils.resolve_brand(
            body.brand, "ANA" if provider_uses_long_brand else body.provider
        )

        if provider_uses_long_brand:
            dict_body["brand"] = brand_name
        else:
            dict_body["brand"] = id

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

        print(response)
        print(type(response))

        return "OK"

        if type(response) == str or isinstance(response, _Element):
            if isinstance(response, _Element):
                response = etree.tostring(response, encoding="unicode")

            elements = utils.resolve_parsel_schema(
                action["struct"], response, action["entry"]
            )

        else:
            elements = utils.zeep_to_dict(response, action["entry"] or None)

            if "struct" in action:
                struct = action["struct"]
                elements = [glom(item, struct) for item in elements]

        # return elements

    if "filter" in action:
        _filter_ = action["filter"]

        # Filter by pipe, check if model match into description
        if _filter_["type"] == "PIPE":
            for item in elements:
                if item["version"].split(" ").count(body.slug):
                    output.append(item)

        # Filter by equal, check if model is equal to value
        if _filter_["type"] == "EQUAL":
            for item in elements:
                if item[_filter_["by"]] == body.slug:
                    del item[_filter_["by"]]
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
