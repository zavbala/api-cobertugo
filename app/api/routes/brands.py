import pandas
from fastapi import APIRouter, Depends, HTTPException, status

from app.resources import strings, utils
from classes.ana import Ana

router = APIRouter()


@router.get("")
async def get_brands():
    frame = pandas.read_csv("data/ANA.csv")
    brands = frame.to_dict(orient="records")

    return brands


@router.get("/{id}/models")
async def get_models(id: str, year: int):
    provider = Ana(brand=id, year=year)
    models = provider.get_models()

    return models
