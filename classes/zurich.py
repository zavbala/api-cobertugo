from datetime import datetime, timedelta

from glom import glom

from app.resources import utils
from classes.soap import Soap

auth = ("pruebasws", "pruebasws")

constants = {
    "agente": "99181",
    "usuario": "pruebasws",
    "numRelacion": "8701022",
}

schema = {
    "id": "id_cobertura",
    "description": "descripcion_cobertura",
    "percentage": "porcentaje_deducible",
}

today = datetime.now().strftime("%Y%m%d")
one_year_later = (datetime.now() + timedelta(days=365)).strftime("%Y%m%d")


class Zurich(Soap):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_versions(self):
        output = []
        brand_id, _ = utils.resolve_brand(self.brand, "ZURICH")
        URL = "https://uat.ezurich.com.mx:443/ZurichWS/autos/consultaClavesVehiculos/publicService"

        sub_brand_id = None
        sub_brands = self.get_brands()

        for item in sub_brands:
            if item["descripcion"] == self.slug:
                sub_brand_id = item["claveSubMarcaAuto"]

        payload = {
            "marca": brand_id,
            "numRequest": "14",
            "modelo": self.year,
            "catalogo": "CAUTO",
            "tipoVehiculo": "1",
            "submarca": sub_brand_id,
            **constants,
        }

        response = self.call("ConsultaClavesZurich", payload, url=URL, credentials=auth)

        for item in response["claveZurich"]:
            output.append(
                {
                    "id": item["clave"],
                    "version": item["descripcion"],
                }
            )

        return output

    def get_brands(self):
        brand_id, _ = utils.resolve_brand(self.brand, "ZURICH")
        URL = "https://uat.ezurich.com.mx:443/ZurichWS/autos/consultaCatalogosAutos/publicService"

        payload = {
            "numRequest": "12",
            "catalogo": "SUBMA",
            "tipoVehiculo": "1",
            "claveMarca": brand_id,
            **constants,
        }

        response = self.call(
            "consultaCatalogoSubMarcaVehiculo", payload, url=URL, credentials=auth
        )

        return response["subMarcaAuto"]

    def get_quotes(self):
        output = []
        URL = "https://uat.ezurich.com.mx/ZurichWS/autos/solCotV2/publicService"

        payload = {
            "num_req": "8",
            "usuario": "pruebasws",
            "idOficina": "10",
            "programaComercial": "8701022",
            "tipoVehiculo": "1",
            "cve_zurich": "016C6664",
            "modelo": self.year,
            "id_estado": self.area,
            "id_ciudad": self.locality,
            "id_tipoValor": "7",
            "id_tipoUso": "1",
            "cve_agente": "99181",
            "tipo_producto": "0",
            "tipo_carga": "0",
            "tipo_persona": "F",
            "edad": self.age,
            "genero": "N",
            "estadoCivil": "7",
            "ocupacion": "1",
            "giro": "1",
            "nacionalidad": "0",
            "id_moneda": "0",
            "fecha_inicio": today,
            "fecha_fin": one_year_later,
            "monto_asegurado": "394900",
            "codigoPostal": self.zip_code,
            "situacionVehiculo": "",
            "mesesVigencia": "12",
            "tipoMovimiento": "1",
            "polizaAnterior": "0",
        }

        response = self.call(
            "getSolicitudCotizacionAutos", payload, url=URL, credentials=auth
        )

        for package in response["PAQUETE"]:
            output.append(
                {
                    "name": package["descripcion_paquete"],
                    "details": [
                        glom(detail, schema) for detail in package["COBERTURA"]
                    ],
                }
            )

        return output
