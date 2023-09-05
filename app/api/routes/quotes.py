import json

import httpx
from fastapi import APIRouter, HTTPException
from lxml import etree
from pydantic import BaseModel
from zeep import Client
from zeep.wsse.username import UsernameToken
from app.resources import strings, utils
from glom import glom


router = APIRouter()


with open("data/Tree.json", "r", encoding="UTF-8") as file:
    plain = file.read()
    providers = json.loads(plain)


class Body(BaseModel):
    age: int
    year: int
    area: str
    brand: str
    gender: str
    provider: str
    locality: str
    zip_code: int


@router.post("")
async def get_quotes(body: Body):
    output = []
    credentials = None
    provider = providers[body.provider]
    action = provider["endpoints"]["quotas"]

    if provider != "ANA":
        brand_id, brand_name = utils.resolve_brand(body.brand, body.provider)
        body.brand = brand_id

    try:
        protocol = provider["protocol"]
    except KeyError:
        protocol = "SOAP"

    if protocol == "REST":
        URL = provider["URL"] + action["path"]

        headers = {
            "Content-Type": strings.CONTENT_TYPE_JSON,
            "Authorization": "Bearer " + provider["token"],
        }

        payload = utils.resolve_my_keys(action["schema"], **body.model_dump())

        if "multiple" in action:
            for item in action["multiple"]["list"]:
                response = httpx.post(
                    URL,
                    json=payload,
                    timeout=3000,
                    headers=headers,
                )

                data = response.json()["data"]
                output.append(data)

        else:
            response = httpx.post(
                URL,
                headers=headers,
                json=action["schema"],
            )

        if "struct" in action:
            struct = action["struct"]

            base = struct["base"]
            items = struct["items"]

            for sample in output:
                numbers = glom(sample, base)
                details = [
                    glom(item, items["schema"]) for item in sample["coverageList"]
                ]

                _dict_ = {**numbers, "details": details}

                return _dict_

                output.append(_dict_)

        return output

    if "authentication" in provider:
        credentials = list(provider["authentication"].values())

    URL = action["URL"] + "?WSDL"
    # payload = utils.resolve_my_keys(action["input"], **body.model_dump())
    # print(payload)
    # return "ALV"

    client = Client(
        URL,
        wsse=UsernameToken(*credentials) if credentials else None,
    )

    method = action["method"]
    response = client.service[method](**payload)

    print(type(response))
    print(response)
