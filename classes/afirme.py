import httpx
from datetime import datetime, timedelta
from app.resources import utils, strings
from classes.rest import Rest
from glom import glom

plans = {
    "9": "Amplia",
    "10": "Limitada",
    "11": "Responsabilidad Civil",
}

quote = {
    "coverage": "premium",
    "percentage": "deductible",
    "description": "description",
}

format = "%d/%m/%Y"
today = datetime.today().timestamp()
one_year_later = (datetime.today() + timedelta(days=365)).strftime(format)

class Afirme(Rest):
    token = None
    # url = "https://www.afirmeseguros.com/gateway"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refresh_token(func):
        def wrapper(self, *args, **kwargs):


            response = self.call(
                "POST",
                self.url + "/oauth/token",
                data={
                    "passFasi": "OMGA5286",
                    "grant_type": "password",
                    "password": "Afirm3#Gat3way",
                    "username": "garfio@cencerro.com",
                    "userFasi": "garfio@cencerro.com",
                },
                auth=("PortalAgentes", "ok00"),
            )

            self.token = response.json()["access_token"]

            return func(self)

        return wrapper

    @refresh_token
    def get_versions(self):
        output = []

        brand_id, _ = utils.resolve_brand(self.brand, "AFIRME")
        payload = {"typeID": "1", "year": self.year, "brandID": brand_id}

        action = self.url + "/catalogs/vehicles/models"

        response = self.call(
            "GET",
            action,
            params=payload,
            headers={"Authorization": f"Bearer {self.token}"},
        )

        result = response.json()["data"]

        for item in result:
            if item["description"].split(" ").count(self.slug):
                output.append(
                    {
                        "id": item["id"],
                        "version": item["description"],
                    }
                )

        return output

    @refresh_token
    def  get_quotes(self):

        action = self.url + "/quote/saveQuotePolicy"
        brand_id, _ = utils.resolve_brand(self.brand, "AFIRME")

        payload = {
            "dataPolicy": {
              "agency": 645,
              "productCode": 632,
              "effectiveDate": today
            },
            "driveZone": {
              "drivingZone": self.area,
              "zipCode": self.zip_code,
            },
            "vehicle": {
              "vehicleType": 1,
              "vehicleCode": 102801,
              "yearOfManufactured": self.year,
              "useOfVehicle": 112,
              "typeVehicleValue": 1,
              "brand": brand_id,
            },
            "packageInfo": {
              "coverageModule": 9,
              "paymentFrequency": 5
            }
        }

        output = []

        for plan in plans.keys():
            payload["packageInfo"]["coverageModule"] = plan
            response = self.call("POST",action,json=payload,headers={"Authorization": f"Bearer {self.token}"})

            result = response.json()
            __list__ = result["data"]["coverageList"]

            output.append({
                "name": plans[plan],
                "details": [glom(x, quote)  for x in __list__]
            })

        return output
