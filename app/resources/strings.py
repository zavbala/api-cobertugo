ANA_GET_VERSIONS = """<?xml version="1.0" encoding="utf-8"?>
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

HDI_GET_VERSIONS = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pub="http://hdi.com.mx/services/public">
    <soapenv:Header/>
    <soapenv:Body>
        <pub:ObtenerVersionesRequest>
            {body}
        </pub:ObtenerVersionesRequest>
    </soapenv:Body>
</soapenv:Envelope>
"""

CONTENT_TYPE_XML = "text/xml; charset=utf-8"

CONTENT_TYPE_JSON = "application/json; charset=utf-8"
