from fastapi import APIRouter, HTTPException
import httpx
import json
from bs4 import BeautifulSoup
from app.resources import strings, utils

with open("data/Tree.json", "r") as file:
    plain = file.read()
    data = json.loads(plain)

router = APIRouter()


@router.get("/{id}/variants")
async def get_variants(id: str, brand: str, year: int):
    provider = data["ANA_SEGUROS"]
    url = provider["url"]

    payload = utils.create_xml_body(
        strings.GET_VARIANTS,
        data={
            "Negocio": 2124,
            "Marca": brand,
            "Submarca": id,
            "Modelo": year,
            "Usuario": 19515,
            "Clave": "G5V3w3RR",
        },
    )

    response = httpx.post(
        url, headers={"Content-Type": strings.CONTENT_TYPE}, data=payload
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    soup = BeautifulSoup(response.text, "xml")
    content = soup.find("VehiculoResult").text

    content = BeautifulSoup(content, "xml")
    items = content.find_all("vehiculo")

    output = []

    for item in items:
        output.append({"name": item.text, "id": item["clave"]})

    return output
