import json
import os

import pandas
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, status
from lxml import etree
from zeep import Client
from uuid import uuid4

from app.resources import strings, utils

with open("data/Tree.json", "r") as file:
    plain = file.read()
    data = json.loads(plain)

router = APIRouter()


@router.get("")
async def get_brands():
    frames = []
    csv_files = [file for file in os.listdir("./data") if file.endswith(".csv")]

    for file in csv_files:
        path = os.path.join("./data", file)
        print(path)

        if file == "QUALITAS.csv":
            continue

        data_frame = pandas.read_csv(path, index_col=0)
        frames.append(data_frame)

    merged = pandas.concat(frames)
    brands = merged.to_dict(orient="records")

    return brands


@router.get("/{id}/models")
async def get_models(id: str, year: int):
    provider = data["ANA"]

    action = provider["endpoints"]["models"]
    URL = provider["URL"] + "?WSDL"

    client = Client(URL)

    payload = {
        **action["input"],
        "Marca": id,
        "Modelo": year,
    }

    response = client.service["SubMarca"](**payload)

    _xml_ = response.split("?>", 1)[1]
    response = etree.fromstring(_xml_)
    soup = utils.zeep_to_bs4(response)

    output = []

    for item in soup.find_all("submarca"):
        output.append({"name": item.text, "id": item["clave"]})

    return output
