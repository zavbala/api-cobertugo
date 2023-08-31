import xml.dom.minidom

from bs4 import BeautifulSoup
from lxml import etree
from zeep.helpers import serialize_object


def create_xml_body(wrapper: str, data: dict, prefix: str = None):
    body = ""

    for key, field in data.items():
        tag = prefix + ":" + key if prefix else key
        body += f"<{tag}>{field}</{tag}>"

    content = wrapper.format(body=body)

    return xml.dom.minidom.parseString(content).toprettyxml()


def resolve_my_keys(schema: dict, **kwargs):
    for key, value in schema.items():
        if value in kwargs:
            schema[key] = kwargs[value]

    return schema


def zeep_to_bs4(response):
    string = etree.tostring(response, encoding="unicode")

    return BeautifulSoup(string, "lxml")


def zeep_to_dict(response, get_key: str = None):
    deserialized = serialize_object(response)

    if get_key:
        deserialized = deserialized[get_key]

    if type(deserialized) == list:
        return [dict(item) for item in deserialized]

    return dict(deserialized)
