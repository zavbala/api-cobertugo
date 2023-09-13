from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from classes import TREE

router = APIRouter()


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

    provider = TREE.get(body.provider)
    instance = provider(**dict_body)
    quotes = instance.get_quotes()

    return quotes
