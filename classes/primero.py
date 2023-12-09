from classes.soap import Soap
from app.resources import utils

constants = {
    # "negocio": "0869",
    "usuario": "agetest",
    "proveedor": "PRVALSEG",
    "token": "F524F89D5ABD4A12E0508F0AAF01A001",
}


class Primero(Soap):
    URL = "https://pruebas.primeroseguros.com/webservices/cotizador"

    def get_versions(self):
        output = []
        brand_id, _ = utils.resolve_brand(self.brand, "PRIMERO")

        payload = {**constants, "marcaVehiculo": f"0{brand_id}"}
        response = self.call("vehiculoSubMarca", payload, url=self.URL)

        for item in response[0]["vehiculoMarcas"]:
            print(item)

            if item["subMarc"] == self.slug:
                pass

        payload = {
            **constants,
            "anio": self.year,
            "subMarca": self.slug,
            "marca": f"0{brand_id}",
            "clave_tipo_vehiculo": "01",
        }

        response = self.call("Vehiculos", payload, url=self.URL)

        return output
