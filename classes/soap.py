from lxml import etree
from lxml.etree import _Element
from zeep import Client, AnyObject
from zeep.wsse.username import UsernameToken

from app.resources import utils


class Soap:
    output = []

    def __init__(
        self,
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

    def client(self, url: str, credentials=None):
        URL = url + "?WSDL"

        return Client(
            URL,
            wsse=UsernameToken(*credentials) if credentials else None,
        )

    @staticmethod
    def parse_response(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # print(result)
            # print(type(result))

            if type(result) == str or isinstance(result, _Element):
                if isinstance(result, _Element):
                    result = etree.tostring(result, encoding="unicode")

                return utils.zeep_to_bs4(result)

            if isinstance(result, AnyObject):
                return utils.zeep_to_dict(result)

            return result

        return wrapper

    @parse_response
    def call(self, method: str, payload: dict, **kwargs):
        return self.client(**kwargs).service[method](**payload)
