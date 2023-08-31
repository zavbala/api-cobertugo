import json

import httpx
import pandas
from fastapi import APIRouter, HTTPException
from lxml import etree
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


@router.post("")
async def get_models(body: ProviderData):
    providers = data.keys()
    file_name = body.provider.upper()

    if body.provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {file_name} not found")

    provider = data[body.provider]
    endpoints = provider["endpoints"]

    try:
        protocol = provider["protocol"]
    except KeyError:
        protocol = "SOAP"

    if protocol == "REST":
        response = httpx.get("https://example.com")
        return response.text

    # URL = provider["URL"] + "?WSDL"
    # client = Client(URL, wsse=UsernameToken("pruebasws", "pruebasws"))

    # print(payload)
    # print(URL)

    brand = None

    if "brands" in endpoints:
        action = endpoints["brands"]
        payload = utils.resolve_my_keys(action["input"], **body.model_dump())

        URL = action["URL"] + "?WSDL"
        client = Client(URL, wsse=UsernameToken("pruebasws", "pruebasws"))

        get_brands = client.service[action["method"]](**payload)
        deserialized = utils.zeep_to_dict(get_brands, "subMarcaAuto")

        for child in deserialized:
            if child["descripcion"] == body.model:
                brand = child["claveSubMarcaAuto"]

    action = endpoints["versions"]

    method = action["method"]
    URL = action["URL"] + "?WSDL"
    client = Client(URL, wsse=UsernameToken("pruebasws", "pruebasws"))

    # payload = utils.resolve_my_keys(action["input"], **body.model_dump())

    print(URL)
    print(method)

    payload = {
        "numRequest": "14",
        "catalogo": "CAUTO",
        "tipoVehiculo": "1",
        "marca": body.brand,
        "submarca": brand,
        "modelo": body.year,
        "numRelacion": "8701022",
        "usuario": "pruebasws",
        "agente": "99181",
    }

    print(payload)

    response = client.service[method](**payload)

    print(response)

    return "ALv"
    # print(type(response))

    if type(response) == str:
        _xml_ = response.split("?>", 1)[1]
        response = etree.fromstring(_xml_)

    soup = utils.parse_zeep(response)

    elements = []

    for item in soup.find_all(action["entry"]):
        computed = {}

        for child in item.contents:
            # Define key - value pairs
            computed[child.name or "slug"] = child.text

        elements.append(computed)

    output = []

    if "filter" in action:
        _filter_ = action["filter"]

        # Filter by pipe, check if model match into description
        if _filter_["type"] == "PIPE":
            for item in elements:
                if item[_filter_["by"]].split(" ").count(body.model) > 0:
                    output.append(item)

        # Filter by equal, check if model is equal to value
        if _filter_["type"] == "EQUAL":
            for item in elements:
                if item[_filter_["by"]] == body.model:
                    output.append(item)

        elements = output

    return elements
