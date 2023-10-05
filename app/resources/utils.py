import json
import re
import xml.dom.minidom
from typing import Union

import pandas
from bs4 import BeautifulSoup
from glom import glom
from lxml import etree
from parsel import Selector
from thefuzz import fuzz
from zeep.helpers import serialize_object


def resolve_parsel_schema(schema: dict, text: str, selector: str):
    output = []
    parsel = Selector(text)

    for item in parsel.css(selector):
        __dict__ = {}

        for key, value in schema.items():
            __dict__[key] = item.css(value).get()

        output.append(__dict__)

    return output


def create_xml_body(wrapper: str, data: dict, prefix: str = None):
    body = ""

    for key, field in data.items():
        tag = prefix + ":" + key if prefix else key
        body += f"<{tag}>{field}</{tag}>"

    content = wrapper.format(body=body)

    return xml.dom.minidom.parseString(content).toprettyxml()


def resolve_my_keys(schema: dict, **kwargs):
    output = schema

    for key, value in schema.items():
        if type(value) == dict:
            for _key, _value in value.items():
                if _value in kwargs:
                    output[key] = {**output[key], _key: kwargs[_value]}
                else:
                    output[key] = {**output[key], _key: _value}

            continue

        if value in kwargs:
            output[key] = kwargs[value]

    return output


def zeep_to_bs4(response):
    return BeautifulSoup(response, "xml")


def zeep_to_dict(response, get_key: str = None):
    deserialized = serialize_object(response)

    if get_key:
        deserialized = deserialized[get_key]

    if type(deserialized) == list:
        return [dict(item) for item in deserialized]

    return dict(deserialized)


def resolve_brand(value: str, provider: str):
    base = pandas.read_csv("data/ANA.csv", index_col=0)
    brand = base.loc[value]["brand"]

    provider_source = provider.upper()
    data_frame = pandas.read_csv(f"data/{provider_source}.csv", index_col=1)

    __id__ = data_frame.loc[brand]["id"]

    return [str(__id__), brand]


def define_my_xml_doc(xml_doc: str, single_line=False, **kwargs):
    for key, value in kwargs.items():
        replacement = "{ " + key + " }"
        xml_doc = xml_doc.replace(replacement, str(value))

    if single_line:
        xml_doc = "".join(xml_doc.splitlines()).replace("  ", "")

    return xml_doc


def normalize(value: str):
    output = value

    door_rgx = r"4\sPUERTAS|4P"
    manual_rgx = r"STD|ESTANDAR"
    automatic_rgx = r"AUT|AUTOMATICO"
    keys = ("4PTAS", "ESTANDAR", "AUTOMATICA")

    for key, expression in enumerate([door_rgx, manual_rgx, automatic_rgx]):
        if match := re.search(expression, output, re.IGNORECASE):
            to_replace = keys[key]
            coincidence = match.group()
            output = output.replace(coincidence, to_replace)

    return output


def fuzzy_match(base: str, elements: list) -> dict:
    ratio, selected = 0, {}

    for element in elements:
        print(f"Comparing {base} with {element['version']}")
        scope = fuzz.token_sort_ratio(base, element["version"])

        print(ratio)

        if scope > ratio:
            ratio = scope
            selected = element

    print(f"Selected: {selected} with {ratio} of similarity")
    return selected
