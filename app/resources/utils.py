import xml.dom.minidom


def create_xml_body(wrapper: str, data: dict, prefix: str = None):
    body = ""

    for key, field in data.items():
        tag = prefix + ":" + key if prefix else key
        body += f"<{tag}>{field}</{tag}>"

    content = wrapper.format(body=body)

    return xml.dom.minidom.parseString(content).toprettyxml()
