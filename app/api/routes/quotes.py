from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from classes import TREE

router = APIRouter()

class Car(BaseModel):
    id: str
    year: int
    brand: str

class User(BaseModel):
    age: int
    gender: str

class Place(BaseModel):
    area: str
    locality: str
    zip_code: int


class Body(BaseModel):
    age: int
    year: int
    area: str
    brand: str
    gender: str
    provider: str
    locality: str
    zip_code: int
    quantity: Optional[int] = 55_000_000




@router.post("")
async def get_quotes(body: Body):
    dict_body = body.model_dump()
    del dict_body["provider"]

    instance = TREE.get(body.provider)

    if body.provider == "AFIRME":
        object = instance(url="https://www.afirmeseguros.com/gateway", **dict_body)
    else:
        object = instance(**dict_body)

    quotes = object.get_quotes()

    return quotes
