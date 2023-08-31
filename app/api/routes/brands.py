import json

import httpx
import pandas
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, status

from app.resources import strings, utils

with open("data/Tree.json", "r") as file:
    plain = file.read()
    data = json.loads(plain)

router = APIRouter()


@router.get("")
async def get_brands():
    data_frame = pandas.read_csv("data/ANA.csv", index_col=0)

    return data_frame.to_dict(orient="records")


@router.get("/{id}/models")
async def get_models(id: str, year: int):
    provider = data["ANA"]
    URL = provider["URL"]

    payload = utils.create_xml_body(
        strings.GET_MODELS,
        data={
            "Negocio": 2124,
            "Marca": id,
            "Modelo": year,
            "Categoria": 100,
            "Usuario": 19515,
            "Clave": "G5V3w3RR",
        },
    )

    response = httpx.post(
        URL,
        headers={
            "Content-Type": "text/xml; charset=utf-8",
        },
        data=payload,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    soup = BeautifulSoup(response.text, "xml")

    content = soup.find("SubMarcaResult").text
    content = BeautifulSoup(content, "xml")

    items = content.find_all("submarca")

    output = []

    for item in items:
        output.append({"name": item.text, "id": item["clave"]})

    return output
