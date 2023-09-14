import httpx

from app.resources import utils, strings
from classes.rest import Rest


class Afirme(Rest):
    token = None

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
