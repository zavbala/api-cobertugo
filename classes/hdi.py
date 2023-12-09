from app.resources import utils
from classes.soap import Soap
from glom import glom

quote = {
    "percentage": "Deducible",
    "coverage": "SumaAsegurada",
    "description": "Descripcion",
}


class Hdi(Soap):
    URL = "http://enterpriseservices.implementation.hdi.com.mx/B2B/Partners/WCF/Autos/PublicServicesAutos.svc"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_versions(self):
        output = []
        brand_id, _ = utils.resolve_brand(self.brand, "HDI")

        payload = {
            "IdNegocio": "",
            "IdMarca": brand_id,
            "IdTipo": self.slug,
            "IdModelo": self.year,
            "IdTipoVehiculo": 4579,
            "usuario": "0695760002",
        }

        result = self.call("ObtenerVersiones", payload, url=self.URL)

        for item in result:
            output.append({"id": item["Clave"], "version": item["Descripcion"]})

        return output

    def get_quotes(self):
        output = []
        brand_id, _ = utils.resolve_brand(self.brand, "HDI")

        payload = {
            "ciudad": "09",
            "estado": "19",
            "idFormaPago": "326",
            "datosVehiculo": {
                "idTipo": "AVEO",
                "idModelo": 2012,
                "idTonelaje": "0",
                "idVersion": "(A)",
                "idMarca": brand_id,
                "idServicio": "4601",
                "idModelo": self.year,
                "tipoVehiculo": "4579",
                "idTransmision": "4534",
                "idZonaCirculacion": "0",
                "numeroSerie": "1141234804",
                "DatosAdicionales": {"CPCirculacion": self.zip_code},
            },
            "SumaAsegurada": "0",
            "usuario": "0695760002",
            "IDTipoSumaAsegurada": "442",
            "obtenerTodosPaquetes": "true",
        }

        entry = "ListaPaquetes.PaquetesCoberturas"

        response = self.call("ObtenerPaquetes", payload, url=self.URL)
        response = glom(response, entry)

        for plan in response:
            output.append(
                {
                    "name": plan["Descripcion"],
                    "details": [
                        glom(x, quote)
                        for x in plan["CoberturasObligatorias"]["Coberturas"]
                    ],
                }
            )

        return output
