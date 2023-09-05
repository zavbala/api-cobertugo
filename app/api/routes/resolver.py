import json

from fastapi import APIRouter
from pydantic import BaseModel
import pandas
import httpx
from zeep import Client
from bs4 import BeautifulSoup

router = APIRouter()

with open("data/Tree.json", "r", encoding="UTF-8") as file:
    plain = file.read()
    providers = json.loads(plain)


class Body(BaseModel):
    year: int
    slug: str
    brand: str
    model: str
    variant: str


@router.post("")
async def resolve(body: Body):
    provider = providers["HDI"]
    URL = provider["URL"] + "?WSDL"
    client = Client(URL)

    # print(URL)

    # return "ALV"

    response = client.service.ObtenerVersiones(
        usuario="0695760002",
        IdTipoVehiculo=4579,
        IdModelo=2019,
        IdMarca=3578,
        IdTipo="AVEO",
    )

    print(response)

    # soup = BeautifulSoup(response, "xml")
    # print(soup.prettify())

    return "ALV"
