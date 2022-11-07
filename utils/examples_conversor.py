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
	"id": "WasteObserved:<uuid of Observer>",
	"type": "WasteObserved",
	"location": {
		"type": "geo:json",
		"value": {
			"type": "Point",
			"coordinates": [
				4.421732917,
				51.21301073
			]
		},
		"metadata": {
			"timestamp": {
				"type": "DateTime",
				"value": "2022-10-19T14:57:39.000Z"
			}
		}
	},
	"address": {
		"type": "PostalAddress",
		"value": {
			"postalCode": "2018",
			"streetAddress": "Lange Kievitstraat n°70",
			"addressCountry": "BE"
		},
		"metadata": {
			"timestamp": {
				"type": "DateTime",
				"value": "2022-10-19T14:57:39.000Z"
			}
		}
	},
	"dateObserved": {
		"type": "DateTime",
		"value": "2022-10-19T14:57:39.000Z",
		"metadata": {}
	},
	"weight": {
		"type": "Number",
		"value": 6.85,
		"metadata": {
			"UnitCode": {
				"type": "string",
				"value": "KGM"
			}
		}
	},
	"grossWeight": {
		"type": "Number",
		"value": 8.85,
		"metadata": {
			"UnitCode": {
				"type": "string",
				"value": "KGM"
			}
		}
	},
	"TareWeight": {
		"type": "Number",
		"value": 2.0,
		"metadata": {
			"UnitCode": {
				"type": "string",
				"value": "KGM"
			}
		}
	},
	"refServiceOrderId": {
		"type": "Relationship",
		"value": "WorkOrder1234"
	}
}
"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
