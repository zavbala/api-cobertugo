import json

import httpx
from fastapi import APIRouter, HTTPException
from lxml import etree
from pydantic import BaseModel
from zeep import Client
from zeep.wsse.username import UsernameToken
from app.resources import strings, utils
from glom import glom
from typing import Optional
from datetime import datetime, timedelta
from zeep import xsd


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
    quantity: Optional[int] = 55_000_000


@router.post("")
async def get_quotes(body: Body):
    output = []
    credentials = None
    provider = providers[body.provider]
    action = provider["endpoints"]["quotas"]

    # if provider != "ANA":
    #     brand_id, brand_name = utils.resolve_brand(body.brand, body.provider)
    #     body.brand = brand_id

    try:
        protocol = provider["protocol"]
    except KeyError:
        protocol = "SOAP"

    # if protocol == "REST":
    #     URL = provider["URL"] + action["path"]

    #     headers = {
    #         "Content-Type": strings.CONTENT_TYPE_JSON,
    #         "Authorization": "Bearer " + provider["token"],
    #     }

    #     payload = utils.resolve_my_keys(action["schema"], **body.model_dump())

    #     if "multiple" in action:
    #         for item in action["multiple"]["list"]:
    #             response = httpx.post(
    #                 URL,
    #                 json=payload,
    #                 timeout=3000,
    #                 headers=headers,
    #             )

    #             data = response.json()["data"]
    #             output.append(data)

    #     else:
    #         response = httpx.post(
    #             URL,
    #             headers=headers,
    #             json=action["schema"],
    #         )

    #     if "struct" in action:
    #         struct = action["struct"]

    #         base = struct["base"]
    #         items = struct["items"]

    #         for sample in output:
    #             numbers = glom(sample, base)
    #             details = [
    #                 glom(item, items["schema"]) for item in sample["coverageList"]
    #             ]

    #             _dict_ = {**numbers, "details": details}

    #             return _dict_

    #             output.append(_dict_)

    #     return output

    if "authentication" in provider:
        credentials = list(provider["authentication"].values())

    # URL = action["URL"] + "?WSDL"
    # # payload = utils.resolve_my_keys(action["input"], **body.model_dump())
    # # print(payload)
    # # return "ALV"

    # client = Client(
    #     URL,
    #     wsse=UsernameToken(*credentials) if credentials else None,
    # )

    # method = action["method"]
    # response = client.service[method](**payload)

    if protocol == "SOAP":
        method = action["method"]

        if "URL" in provider:
            base = provider["URL"]
        else:
            base = action["URL"]

        URL = base + "?WSDL"
        client = Client(URL)

        today = datetime.now()
        one_year = today + timedelta(days=365)

        if body.provider == "QUALITAS":
            with open(
                f"docs/{body.provider.upper()}.xml", "r", encoding="UTF-8"
            ) as file:
                content = file.read()

            payload = {
                "today": today.strftime("%Y-%m-%d"),
                "future": one_year.strftime("%Y-%m-%d"),
                **body.model_dump(),
            }

            doc = utils.define_my_xml_doc(content, **payload)
            # string = etree.tostring(doc, encoding="unicode", pretty_print=True)

            response = client.service[method](xmlEmision=doc)

        if body.provider == "ANA":
            with open(
                f"docs/{body.provider.upper()}.xml", "r", encoding="UTF-8"
            ) as file:
                content = file.read()

            payload = {
                "today": today.strftime("%d/%m/%Y"),
                "future": one_year.strftime("%d/%m/%Y"),
                **body.model_dump(),
            }

            doc = utils.define_my_xml_doc(content, **payload)

            # print(doc)
            # print(type(doc))
            # return "ALV"
            # data =

            xml = etree.fromstring(doc)
            # xml = etree.tostring(xml, encoding="unicode", pretty_print=False)

            # print(xml)

            # return "ALV"

            string = xsd.AnyObject(xsd.String(), xml)
            print(string)
            print(type(string))

            # return "ALV"

        response = client.service[method](
            XML=string, Tipo="Cotizacion", Usuario=19515, Clave="x3J1Sj2Y"
        )

        print(response)
        print(type(response))

        return "ALV"
