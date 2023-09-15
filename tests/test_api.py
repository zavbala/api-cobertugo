import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_get_brands():
    response = client.get("/brands")

    assert response.status_code == 200
    assert len(response.json()) == 35


args = [("CH", 2019), ("HA", 2020), ("BW", 2021), ("AI", 2022)]


@pytest.mark.parametrize("brand,year", args)
def test_get_models(brand, year):
    response = client.get(f"/brands/{brand}/models?year={year}")

    assert response.status_code == 200
    assert len(response.json()) > 0


providers = ["AFIRME", "ZURICH"]


@pytest.mark.parametrize("provider", providers)
def test_get_versions(provider):
    payload = {
        "year": year,
        "slug": slug,
        "brand": brand,
        "model": model,
        "provider": "string",
    }

    response = client.post(f"/models", json=payload)

    assert response.status_code == 200
    assert len(response.json()) > 0
