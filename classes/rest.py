import httpx
from app.resources import strings


class Rest:
    output = []

    def __init__(
        self,
        url=None,
        year=None,
        brand=None,
        slug=None,
        model=None,
        age=None,
        area=None,
        gender=None,
        locality=None,
        zip_code=None,
        quantity=None,
    ):
        self.url = url

        self.slug = slug
        self.year = year
        self.model = model
        self.brand = brand

        self.age = age
        self.area = area
        self.gender = gender
        self.locality = locality
        self.zip_code = zip_code
        self.quantity = quantity

    def call(self, method, url, **kwargs):
        return httpx.request(method, url, timeout=3000, **kwargs)
