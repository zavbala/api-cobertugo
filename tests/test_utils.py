import pytest
from app.resources import utils
from lxml import etree


samples = [
    ("CH", "HDI", ["3578", "CHEVROLET"]),
    ("CH", "ZURICH", ["16", "CHEVROLET"]),
    ("CH", "AFIRME", ["1006", "CHEVROLET"]),
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


docs = [
    (
        """<tag>{ body }</tag>""",
        {"body": "content"},
        "<tag>content</tag>",
    ),
    (
        "<xml><tag>{ body }</tag></xml>",
        {"body": "content"},
        "<xml><tag>content</tag></xml>",
    ),
    (
        '<xml><tag attr="{ body }">content</tag></xml>',
        {"body": "value"},
        '<xml><tag attr="value">content</tag></xml>',
    ),
]


@pytest.mark.parametrize("wrapper,data,expected", docs)
def test_create_xml_document(wrapper, data, expected):
    assert expected == utils.define_my_xml_doc(wrapper, **data)
