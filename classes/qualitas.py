from classes.soap import Soap
from app.resources import strings, utils
from bs4 import Tag


class Qualitas(Soap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_versions(self):
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
                self.output.append(
                    {
                        "id": item.select_one("cTarifa").text,
                        "version": item.select_one("cVersion").text,
                    }
                )

        return self.output

    def get_quotas(self):
        URL = ""
