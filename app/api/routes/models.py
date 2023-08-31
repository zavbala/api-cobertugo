from fastapi import APIRouter, HTTPException
import httpx
import json
from bs4 import BeautifulSoup
from app.resources import strings, utils
from pydantic import BaseModel
import pandas


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
    endpoint = provider["endpoints"]["versions"]

    # provider_frame = pandas.read_csv(f"data/{file_name}.csv", index_col=0)
    # query = provider_frame.loc[provider_frame["brand"] == body.brand]

    # brand_id = query.index[0]
    # wrapper_string = file_name + "_" + provider["wrapper"]

    # payload = utils.create_xml_body(
    #     strings.HDI_GET_VERSIONS,
    #     {
    #         "IdMarca": 3578,
    #         "IdModelo": 2019,
    #         "IdTipo": "AVEO",
    #         "IdTipoVehiculo": 4579,
    #         "usuario": "0695760002",
    #     },
    #     prefix="pub",
    # )

    # payload = utils.create_xml_body(
    #     strings.ANA_GET_VERSIONS,
    #     {
    #         "Negocio": 2124,
    #         "Marca": body.brand,
    #         "Submarca": body.model,
    #         "Modelo": body.year,
    #         "Usuario": 19515,
    #         "Clave": "G5V3w3RR",
    #     },
    # )

    try:
        protocol = provider["protocol"]
    except KeyError:
        protocol = "SOAP"

    if protocol == "REST":
        response = await httpx.get(
            provider["URL"] + endpoint["path"],
            json={"year": body.year, "typeID": "1", "brandID": "1006"},
            headers={
                "Content-Type": strings.CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {provider['token']}",
            },
        )

        print(response.text)

        output = response.json()

        if endpoint["kind"] == "PIPE":
            return [
                item if item.split(" ").count("AVEO") else None
                for item in output["data"]
            ]

    # response = httpx.post(
    #     data=payload,
    #     url=provider["URL"],
    #     headers={"Content-Type": strings.CONTENT_TYPE_XML},
    # )

    # soup = BeautifulSoup(response.text, "xml")
    # entry, item = endpoint["entry"]

    # content = soup.find(entry).text
    # content = BeautifulSoup(content, "xml")
    # items = content.find_all(item)

    # output = []

    # for item in items:
    #     output.append({"name": item.text, "id": item["clave"]})

    # return {
    #     "year": body.year,
    #     "variants": output,
    #     "model": body.model,
    #     "brand": body.brand,
    #     "provider": body.provider,
    # }
