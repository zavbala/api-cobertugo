import httpx
from fastapi import APIRouter, HTTPException

from app.resources import strings, utils

router = APIRouter()


@router.post("")
async def get_packages(provider: str):
    # body = utils.create_xml_body("", {"pub:usuario": ""})

    response = httpx.post(
        "",
        data="",
        headers={"Content-Type": strings.CONTENT_TYPE_XML},
    )

    print(response.text)

    return {"message": "Hello World"}
