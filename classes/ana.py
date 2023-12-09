from datetime import datetime, timedelta
from collections import Counter
from lxml import etree
from bs4 import Tag
from app.resources import utils
from classes.soap import Soap

constants = {
    "Negocio": 2124,
    "Usuario": 19515,
    "Clave": "G5V3w3RR",
}

quota = {
    "prima": "pma",
    "amount": "sa",
    "percentage": "ded",
    "description": "desc",
}

plans = {
"1": "Amplia",
"3": "Limitada",
"4": "Responsabilidad Civil",
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

        slugs = [item["slug"] for item in output]

        # Check for duplicates
        elements = Counter(slugs)

        # Get indexes of duplicates
        duplicate_indexes = {
            key: [index for index, value in enumerate(slugs) if value == key]
            for key, count in elements.items()
            if count > 1
        }

        if duplicate_indexes:
            main, *duplicates = list(duplicate_indexes.values())[0]

            output[main]["id"] = (
                output[main]["id"]
                + "-"
                + "-".join([output[item]["id"] for item in duplicates])
            )

            # Remove duplicates from main list
            for item in duplicates:
                del output[item]

        return output

    def get_versions(self):
        output = []

        payload = {
            "Marca": self.brand,
            "Modelo": self.year,
            **constants,
        }

        for slug in self.model.split("-"):
            payload["Submarca"] = slug
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
            "area": self.area + self.locality,
        }

        docs, output = [], []

        for plan in plans.keys():
            args["plan"] = plan
            document = utils.define_my_xml_doc(xml, single_line=True, **args).replace(" />", "/>")

            docs.append(document)
            tree = etree.fromstring(document)

            payload = {
                "XML": tree,
                "Usuario": 19515,
                "Clave": "x3J1Sj2Y",
                "Tipo": "Cotizacion",
            }

            details = []
            response: Tag = self.call("Transaccion", payload, url=self.URL)

            for item in response.find_all("cobertura"):
                _dict_ = {}

                for key, value in quota.items():
                    _dict_[key] = item[value].strip()

                details.append(_dict_)

            output.append({"name": plans[plan],"details": details})

        return output
