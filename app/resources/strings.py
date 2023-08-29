GET_VARIANTS = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <Vehiculo xmlns="http://tempuri.org/">
            {body}
        </Vehiculo>
    </soap:Body>
</soap:Envelope>
"""

GET_MODELS = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <SubMarca xmlns="http://tempuri.org/">
            {body}
        </SubMarca>
    </soap:Body>
</soap:Envelope>
"""

CONTENT_TYPE = "text/xml; charset=utf-8"