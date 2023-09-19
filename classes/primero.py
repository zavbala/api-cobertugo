from classes.soap import Soap

constants = {
    "usuario": "agetest",
    "proveedor": "PRVALSEG",
    "token": "F524F89D5ABD4A12E0508F0AAF01A001",
}


class Primero(Soap):
    URL = "https://pruebas.primeroseguros.com/webservices/cotizador"

    def get_versions(self):
        output = []

        payload = {
            **constants,
        }

        response = self.call("getVersiones", payload)
