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
	"id": "APDSObservation:Arvoo:<Arvoo.SGID>",
	"type": "APDSObservation",
	"observedMethod": {
		"type": "Text",
		"value": "anpr",
		"metadata": {}
	},
	"observedCredentialType": {
		"type": "Text",
		"value": "license plate",
		"metadata": {}
	},
	"observedCredentialId": {
		"type": "Text",
		"value": "1ENC003",
		"metadata": {}
	},
	"observedCredentialCountry": {
		"type": "Text",
		"value": "BE",
		"metadata": {}
	},
	"observedCredentialConfidence": {
		"type": "Number",
		"value": 851,
		"metadata": {
			"confidenceMethod": {
				"type": "Text",
				"value": "Arvoo"
			}
		}
	},
	"observedCredentialCharacterConfidence": {
		"type": "array",
		"value": [
			"944",
			"851",
			"876",
			"950",
			"932",
			"936",
			"901"
		],
		"metadata": {
			"confidenceMethod": {
				"type": "Text",
				"value": "Arvoo"
			}
		}
	},
	"observer": {
		"type": "Text",
		"value": "Arvoo",
		"metadata": {}
	},
	"observerDescription": {
		"type": "Text",
		"value": "Scangenius Auto-26",
		"metadata": {}
	},
	"creator": {
		"type": "Text",
		"value": "25399",
		"metadata": {}
	},
	"observerCameras": {
		"type": "Array",
		"value": [
			"LF,LB"
		],
		"metadata": {}
	},
	"observationDateTime?": {
		"type": "DateTime",
		"value": "2020-09-11T10:45:00.00Z",
		"metadata": {}
	},
	"observerLocation": {
		"type": "geo:json",
		"value": {
			"type": "Point",
			"coordinates": [
				4.412077,
				51.216632
			]
		},
		"metadata": {
			"timestamp": {
				"type": "DateTime",
				"value": "2020-09-11T10:45:00.00Z"
			}
		}
	},
	"observerLocationPDOP": {
		"type": "Number",
		"value": 0.2959945752,
		"metadata": {
			"UnitCode": {
				"type": "Text",
				"value": "MTR"
			}
		}
	},
	"observerHeading": {
		"type": "Number",
		"value": 175,
		"metadata": {}
	},
	"observerSpeed": {
		"type": "Number",
		"value": 26,
		"metadata": {
			"UnitCode": {
				"type": "Text",
				"value": "KMH"
			}
		}
	},
	"observedLocation": {
		"type": "geo:json",
		"value": {
			"type": "Point",
			"coordinates": [
				4.00412077,
				51.00216632
			]
		},
		"metadata": {
			"timestamp": {
				"type": "DateTime",
				"value": "2020-09-11T10:45:00.00Z"
			}
		}
	},
	"observedLocationPDOP": {
		"type": "Number",
		"value": 0.2959945752,
		"metadata": {
			"UnitCode": {
				"type": "Text",
				"value": "MTR"
			}
		}
	},
	"observedHeading": {
		"type": "Number",
		"value": 175,
		"metadata": {}
	},
	"observedSpeed": {
		"type": "Number",
		"value": -1,
		"metadata": {}
	},
	"images": {
		"type": "array",
		"value": [
			[
				{
					"URL": "mock:http://10.1.0.11:7400/getimage?sgid=8775639&amp;camid=lf&amp;imgreqtype=anpr"
				},
				{
					"camId": "LF"
				},
				{
					"imageContent": "ANPR"
				}
			],
			[
				{
					"URL": "mock:mock:http://10.1.0.11:7400/getimage?sgid=8775639&amp;camid=lf&amp;imgreqtype=overview"
				},
				{
					"camId": "LF"
				},
				{
					"imageContent": "Overview"
				}
			],
			[
				{
					"URL": "mock:http://10.1.0.11:7400/getimage?sgid=8775639&amp;camid=lf&amp;imgreqtype=plate"
				},
				{
					"camId": "LF"
				},
				{
					"imageContent": "Plate"
				}
			],
			[
				{
					"URL": "mock:http://10.1.0.11:7400/getimage?sgid=8775639&amp;camid=plf&amp;distance=-5.22"
				},
				{
					"camId": "LF***NIET PLF"
				},
				{
					"imageContent": "Panorama"
				},
				{
					"distance": -5.22
				}
			]
		],
		"metadata": {}
	}
}
"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
