from pydantic import BaseModel


class Version(BaseModel):
    id: str
    version: str

class Plan(BaseModel):
    pass


class Brand(BaseModel):
    id: str
    slug: str
