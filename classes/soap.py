from lxml import etree
from lxml.etree import _Element
from zeep import AnyObject, Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from zeep.wsse.username import UsernameToken
import os

from app.resources import utils

history = HistoryPlugin()


class Soap:
    MAX_RETRIES = 3

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
            plugins=[history],
            wsse=UsernameToken(*credentials) if credentials else None,
        )

    @staticmethod
    def parse_response(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            print(result)
            print(type(result))

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
        retries = 0

        while retries < self.MAX_RETRIES:
            try:
                result = self.client(**kwargs).service[method](**payload)
                break
            except Fault as e:
                retries += 1

        if retries == self.MAX_RETRIES:
            raise Exception("Max retries reached")

        if os.environ.get("ENVIROMENT") == "development":
            print(history.last_sent)
            print(history.last_received)

        return result
