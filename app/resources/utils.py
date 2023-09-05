import xml.dom.minidom

import pandas
from bs4 import BeautifulSoup
from lxml import etree
from zeep.helpers import serialize_object
from glom import glom
import json
from typing import Union


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

    flag, string = False, None

    if type(response) != str:
        flag = True
        string = etree.tostring(response, encoding="unicode")

    return BeautifulSoup(string if flag else response  , "lxml")


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

    _id_ = data_frame.loc[brand]["id"]

    return str(_id_)

def create_pricing_plan(data: dict, provider:str):

    with open("data/Tree.json", "r") as file:
        plain = file.read()
        data = json.loads(plain)
