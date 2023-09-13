from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from classes import TREE

router = APIRouter()


class ProviderData(BaseModel):
    year: int
    brand: str
    model: str
    provider: str
    slug: Optional[str]


@router.post("")
async def get_models(body: ProviderData):
    dict_body = body.model_dump()
    del dict_body["provider"]

    provider = TREE.get(body.provider)

    if body.provider == "AFIRME":
        instance = provider(url="https://www.afirmeseguros.com/gateway", **dict_body)
    else:
        instance = provider(**dict_body)

    versions = instance.get_versions()

    return {
        "year": body.year,
        "model": body.model,
        "brand": body.brand,
        "provider": body.provider,
        "slug": body.slug,
        "data": versions,
    }
