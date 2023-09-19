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

slugs = [
    (
    "CHEVROLET AVEO LS L4 1.5L 107 CP 4 PUERTAS AUT", # AFIRME
    "CHEVROLET AVEO LS L4 1.5L 107 CP 4PTAS AUTOMATICA"
    ),
    (
        "AVEO LS RADIO L SEDAN AUT AA CD BA 103HP 1.6L 4CIL 4P 5OCUP", # ZURICH
        "AVEO LS RADIO L SEDAN AUTOMATICA AA CD BA 103HP 1.6L 4CIL 4PTAS 5OCUP"
    ),
    (
        "F LT 4P L4 1.6L ABS CD MP3 AC R15 DH STD 5 OCUP", # QUALITAS
        "F LT 4PTAS L4 1.6L ABS CD MP3 AC R15 DH ESTANDAR 5 OCUP"
    ),
    (
        "LS, L4, 1.5L, 107 CP, 4 PUERTAS, AUT", # HDI
        "LS, L4, 1.5L, 107 CP, 4PTAS, AUTOMATICA"
    )
]


@pytest.mark.parametrize("slug,expected", slugs)
def test_normalize_slug(slug, expected):
    assert expected == utils.normalize(slug)


elements =[ (
    "CH CHEVROLET AVEO LS AC ESTANDAR 4PTAS",
    [
        {
          "id": "102801",
          "version": "CHEVROLET AVEO LS L4 1.5L 107 CP 4 PUERTAS AUT"
        },
        {
          "id": "102802",
          "version": "CHEVROLET AVEO LS L4 1.5L 107 CP 4 PUERTAS STD"
        },
        {
          "id": "102810",
          "version": "CHEVROLET AVEO LS L4 1.6L 103 CP 4 PUERTAS STD PAQ K"
        },
        {
          "id": "102803",
          "version": "CHEVROLET AVEO LS L4 1.6L 103 CP 4 PUERTAS AUT PAQ J"
        },
        {
          "id": "102813",
          "version": "CHEVROLET AVEO LT L4 1.5L 107 CP 4 PUERTAS AUT"
        },
        {
          "id": "102814",
          "version": "CHEVROLET AVEO LT L4 1.5L 107 CP 4 PUERTAS STD"
        },
        {
          "id": "102822",
          "version": "CHEVROLET AVEO LT L4 1.6L 103 CP 4 PUERTAS STD PAQ F"
        },
        {
          "id": "102823",
          "version": "CHEVROLET AVEO LT L4 1.6L 103 CP 4 PUERTAS STD PAQ W"
        },
        {
          "id": "102815",
          "version": "CHEVROLET AVEO LT L4 1.6L 103 CP 4 PUERTAS AUT PAQ C"
        },
        {
          "id": "102824",
          "version": "CHEVROLET AVEO LTZ L4 1.5L 107 CP 4 PUERTAS AUT"
        },
        {
          "id": "102825",
          "version": "CHEVROLET AVEO LTZ L4 1.5L 107 CP 4 PUERTAS STD"
        },
        {
          "id": "102826",
          "version": "CHEVROLET AVEO LTZ L4 1.6L 103 CP 4 PUERTAS AUT PAQ E"
        }
    ],
    "CHEVROLET AVEO LS L4 1.5L 107 CP 4PTAS ESTANDAR"
)]

@pytest.mark.parametrize("slug,versions,expected", elements)
def test_fuzzy_match(slug, versions, expected):
    for key, element in enumerate(versions):
        versions[key]["version"] = utils.normalize(element["version"])

    result = utils.fuzzy_match(slug, versions)

    assert expected == result["version"]
