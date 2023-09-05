import json
import os

import pandas
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, status
from lxml import etree
from zeep import Client
from uuid import uuid4
from app.resources import strings, utils

from app.resources import strings, utils

with open("data/Tree.json", "r") as file:
    plain = file.read()
    data = json.loads(plain)

router = APIRouter()


@router.get("")
async def get_brands():

    frame = pandas.read_csv("data/ANA.csv")
    brands = frame.to_dict(orient="records")

    return brands


@router.get("/{id}/models")
async def get_models(id: str, year: int):
    provider = data["ANA"]
    action = provider["endpoints"]["models"]

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
