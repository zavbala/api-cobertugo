import pytest
from app.resources import utils


samples = [
    ("CH", "HDI", ["3578", "CHEVROLET"]),
    ("CH", "ZURICH", ["16", "CHEVROLET"]),
    ("CH", "AFIRME", ["1006", "CHEVROLET"]),
    ("CH", "QUALITAS", ["CH", "CHEVROLET"]),
]


@pytest.mark.parametrize("brand,provider,expected", samples)
def test_get_my_brand_from_csv(brand, provider, expected):
    assert expected == utils.resolve_brand(brand, provider)


dicts = [
    (
        {
            "year": "year",
            "brand": "brand",
            "model": "model",
        },
        {
            "year": 2020,
            "brand": "CH",
            "model": "16",
        },
        {
            "year": 2020,
            "brand": "CH",
            "model": "16",
        },
    ),
    (
        {
            "parent": {
                "year": "year",
            },
            "cousin": {"model": "model"},
        },
        {
            "year": 2020,
            "model": "16",
        },
        {
            "parent": {
                "year": 2020,
            },
            "cousin": {"model": "16"},
        },
    ),
]


@pytest.mark.parametrize("dict,schema,expected", dicts)
def test_resolve_my_keys(dict, schema, expected):
    assert expected == utils.resolve_my_keys(dict, **schema)
