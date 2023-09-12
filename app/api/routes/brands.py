import json

import pandas
from fastapi import APIRouter, Depends, HTTPException, status
from lxml import etree
from zeep import Client

from app.resources import strings, utils

with open("schemas/ANA.json", "r") as file:
    plain = file.read()
    provider = json.loads(plain)

router = APIRouter()


@router.get("")
async def get_brands():
    frame = pandas.read_csv("data/ANA.csv")
    brands = frame.to_dict(orient="records")

    return brands


@router.get("/{id}/models")
async def get_models(id: str, year: int):
    URL = provider["URL"] + "?WSDL"
    client = Client(URL)

    payload = {
        "Marca": id,
        "Modelo": year,
        "Categoria": 100,
        **provider["constants"],
    }

    response = client.service["SubMarca"](**payload)

    _xml_ = response.split("?>", 1)[1]
    response = etree.fromstring(_xml_)
    soup = utils.zeep_to_bs4(response)

    output = []

    for item in soup.find_all("submarca"):
        output.append({"slug": item.text, "id": item["clave"]})

    return output
