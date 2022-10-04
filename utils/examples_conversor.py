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

    def valid_date(datestring):
        import re
        date = datestring.split("T")[0]
        print(date)
        try:
            validDate = re.match('^[0-9]{2,4}[-/][0-9]{2}[-/][0-9]{2,4}$', date)
            print(validDate)
        except ValueError:
            return False

        if validDate is not None:
            return True
        else:
            return False

    keyvaluesDict = keyvaluesPayload
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
            if valid_date(keyvaluesDict[element]):
                # it is a date
                item["format"] = "date-time"
            # it is a string
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

    if "id" in output:
        output["id"] = output["id"]["value"]
    if "type" in output:
        output["type"] = output["type"]["value"]
    if "@context" in output:
        output["@context"] = output["@context"]["value"]
    print(output)
    return output


keyvaluesPayload = {
    "resourceType": "Patient",
    "identifier": [
        {
            "period": {
                "start": "2001-05-06"
            },
            "assigner": {
                "display": "Acme\u202fHealthcare"
            },
            "use": "usual",
            "system": "urn:oid:1.2.36.146.595.217.0.1",
            "value": "12345"
        }
    ],
    "managingOrganization": {
        "reference": "Organization/1"
    },
    "_active": {
        "extension": [
            {
                "url": "http://example.org/fhir/StructureDefinition/recordStatus",
                "valueCode": "archived"
            }
        ]
    },
    "name": [
        {
            "given": [
                "Peter",
                "James"
            ],
            "use": "official",
            "family": "Chalmers"
        },
        {
            "given": [
                "Jim"
            ],
            "use": "usual"
        }
    ],
    "extension": [
        {
            "url": "http://example.org/fhir/StructureDefinition/patientAvatar",
            "valueReference": {
                "reference": "#pic1",
                "display": "Duck image"
            }
        },
        {
            "url": "http://example.org/fhir/StructureDefinition/complexExtensionExample",
            "extension": [
                {
                    "url": "nestedA",
                    "valueCoding": {
                        "system": "http://demo.org/id/4",
                        "code": "AB45",
                        "extension": [
                            {
                                "url": "http://example.org/fhir/StructureDefinition/extraforcodingWithExt",
                                "extension": [
                                    {
                                        "url": "extra1",
                                        "valueString": "extra info"
                                    }
                                ]
                            },
                            {
                                "url": "http://example.org/fhir/StructureDefinition/extraforcodingWithValue",
                                "valueInteger": 45
                            }
                        ]
                    }
                },
                {
                    "url": "nestedB",
                    "id": "q4",
                    "extension": [
                        {
                            "url": "nestedB1",
                            "valueString": "hello"
                        }
                    ]
                }
            ]
        }
    ],
    "modifierExtension": [
        {
            "url": "http://example.org/fhir/StructureDefinition/pi",
            "valueDecimal": 3.141592653589793
        },
        {
            "url": "http://example.org/fhir/StructureDefinition/max-decimal-precision",
            "valueDecimal": 1.00065022141624642
        }
    ],
    "gender": "male",
    "birthDate": "1974-12",
    "deceasedBoolean": True,
    "address": [
        {
            "use": "home",
            "line": [
                "534 Erewhon St"
            ],
            "city": "PleasantVille",
            "state": "Vic",
            "postalCode": "3999"
        }
    ],
    "maritalStatus": {
        "extension": [
            {
                "url": "http://example.org/fhir/StructureDefinition/nullFlavor",
                "valueCode": "ASKU"
            }
        ]
    },
    "multipleBirthInteger": 3,
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n      <table>\n        <tbody>\n          <tr>\n            <td>Name<\/td>\n            <td>Peter James <b>Chalmers<\/b> (&quot;Jim&quot;)<\/td>\n          <\/tr>\n          <tr>\n            <td>Address<\/td>\n            <td>534 Erewhon, Pleasantville, Vic, 3999<\/td>\n          <\/tr>\n          <tr>\n            <td>Contacts<\/td>\n            <td>Home: unknown. Work: (03) 5555 6473<\/td>\n          <\/tr>\n          <tr>\n            <td>Id<\/td>\n            <td>MRN: 12345 (Acme Healthcare)<\/td>\n          <\/tr>\n        <\/tbody>\n      <\/table>\n    <\/div>"
    },
    "contained": [
        {
            "resourceType": "Binary",
            "id": "pic1",
            "contentType": "image/gif",
            "data": "R0lGODlhEwARAPcAAAAAAAAA/+9aAO+1AP/WAP/eAP/eCP/eEP/eGP/nAP/nCP/nEP/nIf/nKf/nUv/nWv/vAP/vCP/vEP/vGP/vIf/vKf/vMf/vOf/vWv/vY//va//vjP/3c//3lP/3nP//tf//vf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEAAAEALAAAAAATABEAAAi+AAMIDDCgYMGBCBMSvMCQ4QCFCQcwDBGCA4cLDyEGECDxAoAQHjxwyKhQAMeGIUOSJJjRpIAGDS5wCDly4AALFlYOgHlBwwOSNydM0AmzwYGjBi8IHWoTgQYORg8QIGDAwAKhESI8HIDgwQaRDI1WXXAhK9MBBzZ8/XDxQoUFZC9IiCBh6wEHGz6IbNuwQoSpWxEgyLCXL8O/gAnylNlW6AUEBRIL7Og3KwQIiCXb9HsZQoIEUzUjNEiaNMKAAAA7"
        },
        {
            "resourceType": "Organization",
            "id": "org3141",
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n      <p>Good Health Clinic<\/p>\n    <\/div>"
            },
            "identifier": [
                {
                    "system": "urn:ietf:rfc:3986",
                    "value": "2.16.840.1.113883.19.5"
                }
            ],
            "name": "Good Health Clinic"
        }
    ],
    "contact": [
        {
            "name": {
                "family": "du Marché",
                "_family": {
                    "extension": [
                        {
                            "url": "http://example.org/fhir/StructureDefinition/qualifier",
                            "valueString": "VV"
                        },
                        {
                            "url": "http://hl7.org/fhir/StructureDefinitioniso-21090#nullFlavor",
                            "valueCode": "ASKU"
                        }
                    ]
                },
                "_given": [
                    {
                        "id": "a3",
                        "extension": [
                            {
                                "url": "http://hl7.org/fhir/StructureDefinition/qualifier",
                                "valueCode": "MID"
                            }
                        ]
                    }
                ],
                "given": [
                    "Bénédicte",
                    "Denise",
                    "Marie"
                ]
            },
            "relationship": [
                {
                    "coding": [
                        {
                            "system": "http://example.org/fhir/CodeSystem/patient-contact-relationship",
                            "code": "partner"
                        }
                    ]
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": "+33 (237) 998327"
                }
            ]
        }
    ],
    "generalPractitioner": [
        {
            "reference": "#org3141"
        }
    ],
    "telecom": [
        {
            "use": "home"
        },
        {
            "system": "phone",
            "value": "(03) 5555 6473",
            "use": "work"
        }
    ]
}

normalizedPayload = """
{
  "id": "urn:ngsi-ld:AirQualityForecast:France-AirQualityForecast-12345_2022-07-01T18:00:00_2022-07-01T00:00:00",
  "type": "AirQualityForecast",
  "address": {
    "type": "Property",
    "value": {
      "addressCountry": "France",
      "postalCode": "06200",
      "addressLocality": "Nice",
      "type": "PostalAddress"
    }
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        7.2032497427380235,
        43.68056738083439
      ]
    }
  },
  "dataProvider": {
    "type": "Property",
    "value": "IMREDD_UCA_Nice"
  },
  "dateIssued": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T10:40:01.00Z"
    }
  },
  "dateRetrieved": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T12:57:24.00Z"
    }
  },
  "validFrom": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T17:00:00.00Z"
    }
  },
  "validTo": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T18:00:00.00Z"
    }
  },
  "validity": {
    "type": "Property",
    "value": "2022-07-01T17:00:00+01:00/2022-07-01T18:00:00+01:00"
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 3
  },
  "airQualityLevel": {
    "type": "Property",
    "value": "moderate"
  },
  "co2": {
    "type": "Property",
    "value": 45,
    "unitCode": "GQ"
  },
  "no2": {
    "type": "Property",
    "value": 69,
    "unitCode": "GQ"
  },
  "o3": {
    "type": "Property",
    "value": 100,
    "unitCode": "GQ"
  },
  "nox": {
    "type": "Property",
    "value": 139,
    "unitCode": "GQ"
  },
  "so2": {
    "type": "Property",
    "value": 11,
    "unitCode": "GQ"
  },
  "pm10": {
    "type": "Property",
    "value": 19,
    "unitCode": "GQ"
  },
  "pm25": {
    "type": "Property",
    "value": 21,
    "unitCode": "GQ"
  },
  "temperature": {
    "type": "Property",
    "value": 12.2
  },
  "relativeHumidity": {
    "type": "Property",
    "value": 0.54
  },
  "windSpeed": {
    "type": "Property",
    "value": 0.64
  },
  "precipitation": {
    "type": "Property",
    "value": 0
  },
  "typeOfLocation": {
    "type": "Property",
    "value": "outdoor"
  },
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://raw.githubusercontent.com/smart-data-models/dataModel.Environment/master/context.jsonld"
  ]
}
"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
