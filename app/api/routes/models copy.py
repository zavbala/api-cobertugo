import json

import httpx
from fastapi import APIRouter, HTTPException
from lxml.etree import _Element
from pydantic import BaseModel
from typing import Optional
from zeep import Client
from zeep.wsse.username import UsernameToken
from glom import glom
from lxml import etree

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

    action = endpoints["versions"]
    payload = utils.resolve_my_keys()

    method = action["method"]

    if protocol == "REST":
        URL = action["URL"] + action["path"]
        response = httpx.request(request=method, url=URL, json=payload)

        if provider == "AFIRME":
            pass

    if protocol == "SOAP":
        URL = action["URL"] + "?WSDL"

        client = Client(URL)
        response = client.service[method](**dict_body)

        if provider == "ANA":
            elements = ""

        if provider == "QUALITAS":
            pass

        if provider == "ZURICH":
            pass

    return {
        "year": body.year,
        "model": body.model,
        "brand": body.brand,
        "provider": body.provider,
        "slug": body.slug,
        "data": elements,
    }
