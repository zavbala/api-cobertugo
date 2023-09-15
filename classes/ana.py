from classes.soap import Soap
from app.resources import strings, utils
from datetime import datetime, timedelta
from lxml import etree
from zeep import xsd, Client

constants = {
    "Negocio": 2124,
    "Usuario": 19515,
    "Clave": "G5V3w3RR",
}

format = "%d/%m/%Y"
today = datetime.today().strftime(format)
one_year_later = (datetime.today() + timedelta(days=365)).strftime(format)


class Ana(Soap):
    URL = "https://server.anaseguros.com.mx/ananetws/service.asmx"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_models(self):
        output = []

        payload = {
            "Categoria": 100,
            "Marca": self.brand,
            "Modelo": self.year,
            **constants,
        }

        response = self.call("SubMarca", payload, url=self.URL)

        for item in response.find_all("submarca"):
            output.append({"slug": item.text, "id": item["clave"]})

        return output

    def get_versions(self):
        output = []

        payload = {
            "Marca": self.brand,
            "Modelo": self.year,
            "Submarca": self.model,
            **constants,
        }

        response = self.call("Vehiculo", payload, url=self.URL)

        for item in response.find_all("vehiculo"):
            output.append({"version": item.text, "id": item["clave"]})

        return output

    def get_quotes(self):
        with open("docs/ANA.xml", "r") as file:
            xml = file.read()

        args = {
            **self.__dict__,
            "today": today,
            "future": one_year_later,
        }

        document = utils.define_my_xml_doc(xml, single_line=True, **args).replace(
            " />", "/>"
        )

        value = xsd.AnyObject(xsd.String(), document)

        payload = {
            "XML": value,
            "Usuario": 19515,
            "Clave": "x3J1Sj2Y",
            "Tipo": "Cotizacion",
        }

        response = self.call("Transaccion", payload, url=self.URL)

        return response
