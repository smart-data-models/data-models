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
    normalizedDict = normalizedPayload
    # normalizedDict = json.loads(normalizedPayload)
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
  "id": "urn:ngsi-ld:QueueMeasurement:id:IEQX:79193255",
  "type": "QueueMeasurement",
  "Occupancy": 58,
  "ProjectedWaitTime": 544.4,
  "Throughput": 384,
  "WaitTime": 645.9,
  "MeasurementDevice": {
    "Name": "",
    "MeasurementDeviceLocation": {
      "Name": ""
    }
  },
  "MeasurementTimePeriod": {
    "EndTime": "2023-03-22T18:59:02Z"
  },
  "PassengerQueue": {
    "Identifier": "1",
    "Name": "1",
    "CheckpointFacility": {
      "Description": "",
      "Identifier": "1bdaec90-7a42-11e7-bb31-be2e44b06b34",
      "Name": "Checkpoint B",
      "CheckpointAreaLocation": "",
      "CheckpointFacilityOperatorParty": "",
      "CheckpointFacilityType": "",
      "ConcourseFacility": {
        "Identifier": "BA/B",
        "Name": "Boarding Area B",
        "TerminalFacility": {
          "Identifier": "T1",
          "Name": "Terminal 1",
          "AirportFacility": {
            "IataCode": "SFO",
            "IcaoCode": "KSFO",
            "Name": "San Francisco InternationalAirport"
          }
        }
      },
      "OperationTimePeriod": ""
    },
    "PassengerProcess": {
      "Name": "",
      "PassengerProcessType": {
        "Code": "",
        "Description": ""
      }
    },
    "QueueLocation": {
      "Name": ""
    },
    "QueueStatus": {
      "Name": ""
    },
    "QueueType": {
      "Code": "",
      "Description": ""
    }
  }
}

normalizedPayload = {
    "id": "urn:ngsi-ld:Catalogue:id:KSLT:97146192",
    "type": "Catalogue",
    "dateCreated": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2023-03-20T18:53:50Z"
        }
    },
    "dateModified": {
        "id": "urn:ngsi-ld:CheckpointFacility:id:MMJG:16938337",
        "type": "CheckpointFacility",
        "Description": "control",
        "Identifier": "control-1",
        "Name": "",
        "CheckpointAreaLocation": {
            "Latitude": 40.42,
            "Longitude": 3.708,
            "Name": "gate 23",
            "Srid": 0,
            "AirportElevation": {
                "Name": "",
                "Value": 571.3,
                "AirportElevationUnitOfMeasurement": {
                    "Name": "Mater"
                }
            },
            "ZoneAreaLocation": {
                "Name": "",
                "TerminalAreaLocation": {
                    "Name": "",
                    "AirportLocation": {
                        "Latitude": 40.42,
                        "Longitude": 3.708,
                        "Name": "gate 23",
                        "Srid": 534
                    }
                }
            }
        },
        "CheckpointFacilityOperatorParty": {
            "Name": ""
        },
        "CheckpointFacilityType": {
            "Code": "",
            "Description": ""
        },
        "ConcourseFacility": {
            "Identifier": "",
            "Name": "",
            "TerminalFacility": {
                "Identifier": "terminal 1",
                "Name": "",
                "AirportFacility": {
                    "IataCode": "BMA",
                    "IcaoCode": "ESSB",
                    "Name": ""
                }
            }
        },
        "OperationTimePeriod": {
            "ClosingTime": "23:59",
            "OpeningTime": "0:00"
        }
    },
    "@context": [
        "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
    ]
}

# payload = normalized2keyvalues(normalizedPayload)
# print(payload)
# with open("example-normalized.json", "w") as file:
#     json.dump(payload, file)

schema = keyvalues2normalized(keyvaluesPayload)
with open("keyvalues.json", "w") as file:
    json.dump(schema, file)
