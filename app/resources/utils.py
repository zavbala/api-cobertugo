import xml.dom.minidom

def create_xml_body(wrapper: str, data: dict):
    
    body = ""

    for key, field in data.items():
        body += f"<{key}>{field}</{key}>"

    content = wrapper.format(body=body)
    
    return xml.dom.minidom.parseString(content).toprettyxml()