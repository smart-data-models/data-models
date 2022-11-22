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
import json

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
    with open("output.json", "w") as outputfile:
        rawoutput = json.dumps(output, indent=4)
        outputfile.write(rawoutput)
    return output


keyvaluesPayload = {
  "id": "https://smart-data-models.github.io/IUDX/MosquitoDensity/schema.json",
  "type": [
    "MosquitoDensity"
  ],
  "deviceID": "VDFWitw@B",
  "deviceSimNumber": "861123052561188",
  "location": {
    "type": "Point",
    "coordinates": [
      76.9578654,
      8.487284
    ]
  },
  "speciesName": "Culex quinquefasciatus",
  "speciesTotal": 3,
  "femaleTotal": 2,
  "maleTotal": 1,
  "observationDateTime": "2022-09-18T23:59:59+05:30",
  "airTemperature": {
    "instValue": 24.88
  },
  "precipitation": 0,
  "deviceInfo": {
    "rfID": "5634684",
    "deviceBatteryStatus": "Connected",
    "deviceName": "SL1",
    "deviceID": "43",
    "measurand": "6",
    "deviceSimNumber": "6755375727",
    "deviceModel": {
      "brandName": "abc",
      "manufacturerName": "xyz",
      "modelName": "SL1",
      "modelURL": "www.abcstreetlight.com"
    }
  },
  "@context": [
    "iudx:MosquitoDensity",
    "https://raw.githubusercontent.com/smart-data-models/dataModel.Environment/master/context.jsonld"
  ]
}

normalizedPayload = """
{
  "id": "urn:ngsi-ld:FishContainment:1",
  "type": "FishContainment",
  "category": {
    "type": "Property",
    "value": "Tank"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        0,
        0
      ]
    }
  },
  "refSump": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Sump:1"
  },
  "refFarm": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Farm:1"
  },
  "depth": {
    "type": "Property",
    "value": 10,
    "unitCode": "MTR"
  },
  "videoStream": {
    "type": "Property",
    "value": "stream URL",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:camera:01"
    },
    "depth": {
      "type": "Property",
      "value": 10,
      "unitCode": "MTR"
    }
  },
  "temperature": [
    {
      "type": "Property",
      "value": 15.2,
      "unitCode": "CEL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:temperature:Device:01"
    },
    {
      "type": "Property",
      "value": 16.1,
      "unitCode": "CEL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 5,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:Device:02"
      },
      "datasetId": "urn:ngsi-ld:Dataset:temperature:Device:02"
    }
  ],
  "dissolvedOxygen": [
    {
      "type": "Property",
      "value": 80,
      "unitCode": "P1",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:dissolvedOxygen:P1:Device:01"
    },
    {
      "type": "Property",
      "value": 5.4,
      "unitCode": "M1",
      "observedAt": "2020-08-31T11:31:29.000Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:dissolvedOxygen:M1:Device:01"
    }
  ],
  "pH": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "Q30",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:pH:Device:01"
    }
  ],
  "redoxPotential": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "2Z",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:redoxPotential:Device:01"
    }
  ],
  "turbidity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "NTU",
      "observedAt": "2020-06-26T21:32:52z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:turbidity:NTU:Device:01"
    },
    {
      "type": "Property",
      "value": 0,
      "unitCode": "FNU",
      "observedAt": "2020-08-31T11:31:29.000Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:turbidity:FNU:Device:01"
    }
  ],
  "conductivity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "NTU",
      "observedAt": "2020-06-26T21:32:52+02:00",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:aquabox:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:conductivity:NTU:aquabox01"
    }
  ],
  "salinity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "GL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:salinity:GL:Device:01"
    }
  ],
  "totalDissolvedSolids": [
    {
      "type": "Property",
      "value": 35404,
      "unitCode": "G42",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:totalDissolvedSolids:G42:Device:01"
    }
  ],
  "marineCurrents": {
    "type": "Property",
    "value": "NA",
    "observedAt": "2021-05-04T08:30:00Z"
  },
  "feedingOperation": {
    "type": "Property",
    "refFeeder": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Feeder:AUTO"
    },
    "observation": {
      "type": "Property",
      "value": "NA"
    },
    "threats": {
      "type": "Property",
      "value": "NA"
    },
    "value": 10,
    "observedAt": "2021-05-04T08:30:00Z",
    "unitCode": "KGM",
    "endedAt": {
      "type": "Property",
      "value": {
        "type": "DateTime",
        "@value": "2021-05-04T18:00:00Z"
      }
    },
    "startedAt": {
      "type": "Property",
      "value": {
        "type": "DateTime",
        "@value": "2021-05-04T08:30:00Z"
      }
    }
  },
  "fishDensity": [
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean0To1",
      "value": -26.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean1To2",
      "value": -24.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean2To3",
      "value": -15.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean3To4",
      "value": -18.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean4To5",
      "value": -27.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean5To6",
      "value": -26.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean6To7",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean7To8",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean8To9",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean9o10",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    }
  ],
  "fishSpeed": {
    "type": "Property",
    "value": 25.0,
    "unitCode": "",
    "observedAt": "2021-10-19T14:22:19Z"
  },
  "fishDirection": {
    "type": "Property",
    "value": "SW",
    "observedAt": "2021-10-19T14:22:19Z"
  },
  "@context": [
    "https://raw.githubusercontent.com/smart-data-models/data-models/master/context.jsonld"
  ]
}
"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
