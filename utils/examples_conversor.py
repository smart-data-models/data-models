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

    print(output)
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
  "id": "a88c6069-86c4-4c09-8621-fc5c58f216e0",
  "type": "zone",
  "additionalInfo": [
    {
      "name": "Farm2FeedTray",
      "value": "4"
    },
    {
      "name": "Farm2ValveId",
      "value": ""
    },
    {
      "name": "Farm2DepartmentId",
      "value": "11"
    }
  ],
  "arrivalTimestamp": "2020-04-14T22:00:00.000Z",
  "avgGrowth": 1.0,
  "avgWeight": 45.5,
  "buildingId": "f6ce5251-e959-4269-9040-8056c6a093d9",
  "co2": 20,
  "companyId": "1401c9e0-c441-4bd1-b8d3-fb1194479aa7",
  "empty": false,
  "farmId": "7438345c-fdff-45c9-a02f-1d764cbc03a7",
  "feedConsumption": 8.3,
  "humidity": 0.7,
  "lastUpdate": 1589841011000,
  "luminosity": 3,
  "name": "",
  "numAnimals": 22,
  "outputFeed": 8.2,
  "parentZoneId": "f0ddd929-5a18-479b-9ad6-5947cc2cd05b",
  "sex": "",
  "startWeight": 26,
  "temperature": 25,
  "waterConsumption": 23,
  "weightStDev": 2.3
}
"""


normalizedPayload = """
    {
      "id": "urn:ngsi-ld:PhotovoltaicDevice:PhotovoltaicDevice:MNCA-PV-T2-R-012",
      "type": "PhotovoltaicDevice",
      "name": {
        "type": "Property",
        "value": "DEVICE-PV-T2-R-012"
      },
      "alternateName": {
        "type": "Property",
        "value": "AirPort – global Observation"
      },
      "description": {
        "type": "Property",
        "value": "Photo-voltaic Device description"
      },
      "location": {
        "type": "GeoProperty",
        "value": {
          "type": "Point",
          "coordinates": [
            43.664810,
            7.196545
          ]
        }
      },
      "address": {
        "type": "Property",
        "value": {
          "addressCountry": "FR",
          "addressLocality": "Nice",
          "streetAddress": "Airport - Terminal 2 - Roof 2 - Local  12"
        }
      },
      "areaServed": {
        "type": "Property",
        "value": "Nice Aeroport"
      },
      "refDevice": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:Device:PV-T2-R-012"
      },
      "dateLastReported": {
        "type": "Property",
        "value": {
          "type": "DateTime",
          "value": "2020-05-17T09:47:00Z"
        }
      },
      "brandname": {
        "type": "Property",
        "value": "Canadian Solar"
      },
      "modelName": {
        "type": "Property",
        "value": "CS6P-270P"
      },
      "manufacturerName": {
        "type": "Property",
        "value": "Canadian Solar EMEA GmbH,"
      },
      "serialNumber": {
        "type": "Property",
        "value": [
          "CSPV270P-SN1804L6J34Z8742H",
          "CSPV270P-SN1804L6J34Z8743H",
          "CSPV270P-SN1804L6J34Z8744H",
          "CSPV270P-SN1804L6J34Z8745H",
          "CSPV270P-SN1804L6J34Z8746H"
        ]
      },
      "application": {
        "type": "Property",
        "value": "electric"
      },
      "cellType": {
        "type": "Property",
        "value": "polycrystalline"
      },
      "installationMode": {
        "type": "Property",
        "value": "roofing"
      },
      "installationCondition": {
        "type": "Property",
        "value": [
          "extremeHeat",
          "extremeCold",
          "extremeClimate",
          "desert"
        ]
      },
      "possibilityOfUsed": {
        "type": "Property",
        "value": "stationary"
      },
      "integrationMode": {
        "type": "Property",
        "value": "IAB"
      },
      "documentation": {
        "type": "Property",
        "value": "https://www.myDevicePV.Cn"
      },
      "owner": {
        "type": "Property",
        "value": [
          "Airport-Division Maintenance"
        ]
      },
      "cellDimension": {
        "type": "Property",
        "value": {
          "length": 16.0,
          "width": 9.0,
          "thickness": 2.3
        }
      },
      "moduleNbCells": {
        "type": "Property",
        "value": 60
      },
      "moduleDimension": {
        "type": "Property",
        "value": {
          "length": 1600,
          "width": 975,
          "thickness": 3.75
        }
      },
      "panelNbModules": {
        "type": "Property",
        "value": 1
      },
      "panelDimension": {
        "type": "Property",
        "value": {
          "length": 1638,
          "width": 982,
          "thickness": 40
        }
      },
      "panelWeight": {
        "type": "Property",
        "value": 18
      },
      "arealWeight": {
        "type": "Property",
        "value": 32
      },
      "maxPressureLoad": {
        "type": "Property",
        "value": {
          "hail": 2500,
          "snow": 5400,
          "wind": 2400
        }
      },
      "NominalPower": {
        "type": "Property",
        "value": 270
      },
      "MaximumSystemVoltage": {
        "type": "Property",
        "value": 1000
      },
      "applicationClass": {
        "type": "Property",
        "value": "A"
      },
      "fireClass": {
        "type": "Property",
        "value": "C"
      },
      "pTCClass": {
        "type": "Property",
        "value": 92.1
      },
      "nTCClass": {
        "type": "Property",
        "value": 88.3
      },
      "protectionIP": {
        "type": "Property",
        "value": "IP67"
      },
      "moduleSTC": {
        "type": "Property",
        "value": {
          "Pmax": 270,
          "Umpp": 30.8,
          "Impp": 8.75,
          "Uoc": 37.9,
          "Isc": 9.32
        }
      },
      "moduleNOCT": {
        "type": "Property",
        "value": {
          "Pmax": 196,
          "Umpp": 28.1,
          "Impp": 6.97,
          "Uoc": 34.8,
          "Isc": 7.55
        }
      },
      "moduleYieldRate": {
        "type": "Property",
        "value": 16.79
      },
      "panelOperatingTemperature": {
        "type": "Property",
        "value": {
          "min": -40,
          "max": 85
        }
      },
      "cellOperatingTemperature": {
        "type": "Property",
        "value": {
          "min": 45,
          "max": 2
        }
      },
      "temperatureCoefficient": {
        "type": "Property",
        "value": {
          "Pmax": -0.41,
          "Uoc": -0.31,
          "Isc": 0.053
        }
      },
      "performanceLowIrradiance": {
        "type": "Property",
        "value": 96.5
      },
      "panelLifetime": {
        "type": "Property",
        "value": 30
      },
      "panelYieldCurve": {
        "type": "Property",
        "value": [
          "95.0",
          "92.5",
          "90.0",
          "87.5",
          "85.0",
          "80.0"
        ]
      },
      "panelYieldRate": {
        "type": "Property",
        "value": 0.5
      },
      "panelTiltReference": {
        "type": "Property",
        "value": {
          "min": 28,
          "max": 37
        }
      },
      "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ]
    }
    """

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
