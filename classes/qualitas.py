from classes.soap import Soap
from app.resources import utils
from bs4 import Tag
from datetime import datetime, timedelta

format = "%Y-%m-%d"
today = datetime.today().strftime(format)
one_year_later = (datetime.today() + timedelta(days=365)).strftime(format)


class Qualitas(Soap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_versions(self):
        output = []
        URL = "http://qbcenter.qualitas.com.mx/wsTarifa/wsTarifa.asmx"
        _, brand_name = utils.resolve_brand(self.brand, "ANA")

        payload = {
            "cTarifa": "LINEA",
            "cCategoria": "100",
            "cUsuario": "LINEA",
            "cModelo": self.year,
            "cMarca": brand_name,
        }

        response: Tag = self.call("listaTarifas", payload, url=URL)

        for item in response.find_all("Elemento"):
            if item.select_one("cTipo").text.split().count(self.slug):
                output.append(
                    {
                        "id": item.select_one("cTarifa").text,
                        "version": item.select_one("cVersion").text,
                    }
                )

        return output

    def get_quotes(self):
        URL = "https://qa.qualitas.com.mx:8443/WsEmision/WsEmision.asmx"

        with open("docs/dummy.xml") as file:
            xml = file.read()

        args = {
            **self.__dict__,
            "today": today,
            "future": one_year_later,
        }

        # document = utils.define_my_xml_doc(xml, **args).replace(" />", "/>")
        response = self.call("obtenerNuevaEmision", {"xmlEmision": xml}, url=URL)

        return response
