from app.resources import utils


def test_create_xml_body():
    wrapper = """<?xml version="1.0" encoding="utf-8"?>
  <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
      <Vehiculo xmlns="http://tempuri.org/">
        {body}
      </Vehiculo>
    </soap:Body>
  </soap:Envelope>
"""

    result = utils.create_xml_body(
        wrapper,
        data={
            "Negocio": 2124,
            "Marca": "1006",
            "Submarca": "1006",
            "Modelo": 2019,
            "Usuario": 19515,
            "Clave": "G5V3w3RR",
        },
    )

    print(result)
