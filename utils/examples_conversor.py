################################################################################
#  Licensed to the FIWARE Foundation (FF) under one
#  or more contributor license agreements. The FF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# This program takes either a keyvalues payload and converts it into a normalized version and the other way round


def normalized2keyvalues(normalizedPayload):
    import json


    normalizedDict = json.loads(normalizedPayload)
    output = {}
    # print(normalizedDict)
    for element in normalizedDict:
        print(normalizedDict[element])
        try:
            value = normalizedDict[element]["value"]
            output[element] = value
        except:
            output[element] = normalizedDict[element]

    print(json.dumps(output, indent=4, sort_keys=True))
    return output


def keyvalues2normalized(keyvaluesPayload):
    import json

    keyvaluesDict = json.loads(keyvaluesPayload)
    output = {}
    # print(normalizedDict)
    for element in keyvaluesDict:
        item = {}
        print(keyvaluesDict[element])
        if isinstance(keyvaluesDict[element], list):
            # it is an array
            item["type"] = "array"
            item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], dict):
            # it is an object
            item["type"] = "object"
            item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], str):
            # it is an string
            item["type"] = "string"
            item["value"] = keyvaluesDict[element]
        elif keyvaluesDict[element] == True:
            # it is an boolean
            item["type"] = "boolean"
            item["value"] = "true"
        elif keyvaluesDict[element] == False:
            # it is an boolean
            item["type"] = "boolean"
            item["value"] = "false"
        elif isinstance(keyvaluesDict[element], int) or isinstance(keyvaluesDict[element], float):
            # it is an number
            item["type"] = "number"
            item["value"] = keyvaluesDict[element]
        else:
            print("*** other type ***")
            print("I do now know what is it")
            print(keyvaluesDict[element])
            print("--- other type ---")
        output[element] = item

    print(output)
    return output




keyvaluesPayload = """
{
  "id": "urn:ngsi-ld:CatalogueRecordDCAT-AP:id:KFTL:88140679",
  "dateCreated": "2020-11-02T21:25:54Z",
  "dateModified": "2021-07-02T18:37:55Z",
  "source": "",
  "name": "",
  "alternateName": "",
  "description": "Catalogue record of the solar system open data portal",
  "dataProvider": "european open data portal",
  "owner": [
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:ISXP:07320625",
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:BQMW:23610768"
  ],
  "seeAlso": [
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:FVCU:03753474",
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:AIEC:73224831"
  ],
  "location": {
    "type": "Point",
    "coordinates": [
      36.633152,
      -85.183315
    ]
  },
  "address": {
    "streetAddress": "2, rue Mercier",
    "addressLocality": "Luxembourg",
    "addressRegion": "Luxembourg",
    "addressCountry": "Luxembourg",
    "postalCode": "2985",
    "postOfficeBoxNumber": ""
  },
  "areaServed": "European Union and beyond",
  "type": "CatalogueRecordDCAT-AP",
  "primaryTopic": "Public administration",
  "modificationDate": "2021-07-02T18:37:55Z",
  "applicationProfile": "DCAT Application profile for data portals in Europe",
  "changeType": "First version",
  "listingDate": "2021-07-02T18:37:55Z",
  "language": [
    "EN",
    "ES"
  ],
  "sourceMetadata": "",
  "title": [
    "Example of catalogue record",
    "Ejemplo de registro de catálogo"
  ]
}
"""


normalizedPayload = """
{
    "@context": [
        "https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.json",
        "https://raw.githubusercontent.com/GSMADeveloper/NGSI-LD-Entities/master/examples/Machine-context.jsonld"
    ],
    "id": "urn:ngsi-ld:Machine:9166c528-9c98-4579-a5d3-8068aea5d6c0",
    "type": "Machine",
    "createdAt": "2017-01-01T01:20:00Z",
    "modifiedAt": "2017-05-04T12:30:00Z",
    "source": "https://source.example.com",
    "dataProvider": "https://provider.example.com",
    "entityVersion": 2.0,
    "machineModel": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:MachineModel:00b42701-43e1-482d-aa7a-e2956cfd69c3"
    },
    "serialNumber": {
        "type": "Property",
        "value": "X9923456789F"
    },
    "assetIdentifier": {
        "type": "Property",
        "value": "ID12345"
    },
    "supplierName": {
        "type": "Property",
        "value": "ACME NorthEast Inc."
    },
    "countryOfManufacture": {
        "type": "Property",
        "value": "UK"
    },
    "factory": {
        "type": "Property",
        "value": "N9"
    },
    "firstUsedAt": {
        "type": "Property",
        "value": "2017-05-04T10:18:16Z"
    },
    "installedAt": {
        "type": "Property",
        "value": "2017-05-04T10:18:16Z"
    },
    "manufacturedAt": {
        "type": "Property",
        "value": "2017-05-04T10:18:16Z"
    },
    "description": {
        "type": "Property",
        "value": "Industrial machine to create plastic bottles"
    },
    "owner": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:Person:a498182c-47c0-11e8-be4e-2c4d549a1ab2",
            "urn:ngsi-ld:Organization:abb20712-47c0-11e8-8742-2c4d549a1ab2"
        ]
    },
    "hardwareVersion": {
        "type": "Property",
        "value": "2.1"
    },
    "firmwareVersion": {
        "type": "Property",
        "value": "A.10"
    },
    "softwareVersion": {
        "type": "Property",
        "value": "8.5.C"
    },
    "osVersion": {
        "type": "Property",
        "value": "10A"
    },
    "supportedProtocols": {
        "type": "Property",
        "value": [
            "HTTP",
            "HTTPS",
            "FTP"
        ],
        "observedAt": "2017-05-04T12:30:00Z"
    },
    "building": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Building:8683b757-649c-49e0-ac89-ad392c9a0d0c"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [
                -104.99404,
                39.75621
            ]
        }
    },
    "subscriptionServices": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:SubscriptionService:0d95b03c-47c1-11e8-99fd-2c4d549a1ab2",
            "urn:ngsi-ld:SubscriptionService:1527d0fa-47c1-11e8-8fb1-2c4d549a1ab2"
        ]
    },
    "online": {
        "type": "Property",
        "value": true,
        "observedAt": "2017-05-04T12:30:00Z"
    },
    "status": {
        "type": "Property",
        "value": "SC1001",
        "observedAt": "2017-05-04T12:30:00Z"
    },
    "batteryLevel": {
        "type": "Property",
        "value": 0.7,
        "observedAt": "2017-05-04T12:30:00Z"
    },
    "installationNotes": {
        "type": "Property",
        "value": {
            "value": "Installed according to manufacturer instructions.",
            "docUri": "http://example.com/sample/machine-instructions.pdf"
        }
    },
    "voltage": {
        "type": "Property",
        "value": 220,
        "unitCode": "VLT",
        "observedAt": "2016-08-08T10:18:16Z"
    },
    "current": {
        "type": "Property",
        "value": 20,
        "unitCode": "AMP",
        "observedAt": "2016-08-08T10:18:16Z"
    },
    "power": {
        "type": "Property",
        "value": 4.4,
        "unitCode": "KWT",
        "observedAt": "2016-08-08T10:18:16Z"
    },
    "rotationalSpeed": {
        "type": "Property",
        "value": 10,
        "unitCode": "RPM",
        "observedAt": "2016-08-08T10:18:16Z"
    }
}
"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
