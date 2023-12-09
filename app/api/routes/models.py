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


@router.get("/{id}/versions")
async def get_versions_by_model(id: str, brand: str, year: int, slug: str, provider: Optional[str] = "ANA"):
    instance = TREE.get(provider)

    dict_body = {
        "model": id,
        "year": year,
        "slug": slug,
        "brand": brand,
    }

    if provider == "AFIRME":
        object = instance(url="https://www.afirmeseguros.com/gateway", **dict_body)
    else:
        object = instance(**dict_body)

    versions = object.get_versions()

    return {
        "model": id,
        "year": year,
        "slug": slug,
        "brand": brand,
        "data": versions,
        "provider": provider,
    }
