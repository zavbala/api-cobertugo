from app.resources import utils
from classes.soap import Soap


class Hdi(Soap):
    URL = "http://enterpriseservices.implementation.hdi.com.mx/B2B/Partners/WCF/Autos/PublicServicesAutos.svc"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_versions(self):
        output = []
        brand_id, _ = utils.resolve_brand(self.brand, "HDI")

        payload = {
            "usuario": "0695760002",
            "IdTipoVehiculo": 4579,
            "IdModelo": self.year,
            "IdMarca": brand_id,
            "IdTipo": self.slug,
            "IdNegocio": "",
        }

        result = self.call("ObtenerVersiones", payload, url=self.URL)

        for item in result:
            output.append({"id": item["Clave"], "version": item["Descripcion"]})

        return output

    def get_quotes(self):
        brand_id, _ = utils.resolve_brand(self.brand, "HDI")

        payload = {
            "IDTipoSumaAsegurada": self.quantity,
            "estado": "0",
            "idFormaPago": "",
            "datosVehiculo": {
                "idVehiculo": "",
                "idMarca": brand_id,
                "idModelo": self.year,
                "numeroSerie": "",
                "idZonaCirculacion": "",
                "idTonelaje": "",
                "idServicio": "",
                "DatosAdicionales": {"CPCirculacion": self.zip_code},
            },
            "listaPaquetesACalcular": {"StringArray": {"string": "25"}},
            "obtenerTodosPaquetes": "false",
            "usuario": "0695760002",
        }

        response = self.call("ObtenerPaquetes", payload, url=self.URL)

        return response
