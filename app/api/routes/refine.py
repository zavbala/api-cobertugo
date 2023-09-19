from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from app.models.app import Version
from app.resources import strings, utils


class Input(BaseModel):
    provider: str
    elements: List[Version]

class Body(BaseModel):
    slug: str
    providers: List[Input]


router = APIRouter()



@router.post("")
async def refine(body: Body):
    output = []
    input = body.model_dump()

    for provider in input["providers"]:
        list = provider["elements"]

        for key, element in enumerate(list):
            version = element["version"]
            list[key]["version"] = utils.normalize(version)

        computed = utils.fuzzy_match(body.slug, list)
        output.append({"provider": provider["provider"],"computed": computed})

    return output
