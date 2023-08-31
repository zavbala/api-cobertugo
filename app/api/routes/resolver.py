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
    # file = pandas.read_csv("data/ANA_SEGUROS.csv", index_col=0)
    # brand = file.loc[body.brand]["brand"]

    # provider = providers["AFIRME"]
    # URL = provider["URL"] + provider["endpoints"]["models"]["URL"]

    # response = httpx.get(
    #     URL,
    #     params={"year": body.year, "brandID": "1006", "typeID": "1"},
    #     headers={
    #         "Content-Type": "application/json; charset=utf-8",
    #         "Authorization": f"Bearer {provider['token']}",
    #     },
    # )

    # output = []
    # data = response.json()

    # for item in data["data"]:
    #     if item["description"].split(" ").count(body.variant) > 0:
    #         output.append({"name": item["description"], "id": item["id"]})

    provider = providers["HDI"]
    URL = provider["URL"] + "?WSDL"
    client = Client(URL)

    # response = client.service.Marca(2124, 335, "001", 19515, "G5V3w3Rr")
    # response = client.service.Vehiculo(2124, "CH", "035", 2019, 19515, "G5V3w3RR")

    response = client.service.ObtenerMarcas("0695760002", 4579, 2019)

    print(type(response.status_code))

    soup = BeautifulSoup(response, "xml")
    print(soup.prettify())

    return "ALV"
