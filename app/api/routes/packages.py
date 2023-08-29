from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/{provider}")
async def get_packages():
    pass