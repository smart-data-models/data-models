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
	"id": "https://smart-data-models.github.io/SmartWater/WaterDistributionNetwork/schema.json",
	"type": "WaterDistributionNetwork",
	"tankDiameter": 10,
	"totalML": 250,
	"tankCapacity": 500,
	"waterFlow": 14,
	"tankBreadth": 50,
	"tankDepth": 200,
	"flowrate": 70,
	"tankLength": 300,
	"waterTemperature": 20,
	"waterPressure": 5,
	"turbidity": {
		"avgOverTime": 14,
		"maxOverTime": 23,
		"instValue": 34,
		"minOverTime": 12
	},
	"cl": {
		"avgOverTime": 6,
		"maxOverTime": 20,
		"instValue": 12,
		"minOverTime": 23
	},
	"pH": {
		"avgOverTime": 6,
		"maxOverTime": 8,
		"instValue": 7,
		"minOverTime": 6
	},
	"deviceInfo": {
		"rfID": "345438",
		"deviceBatteryStatus": "Connected",
		"deviceName": " Device 4",
		"deviceID": "234",
		"measurand": "2",
		"deviceSimNumber": "9883829934",
		"deviceModel": {
			"brandName": "Trumen Technologies Private Limited",
			"manufacturerName": "Trumen Technologies Private Limited",
			"modelName": "Model 4",
			"modelURL": "https://trumen.in/"
		}
	},
	"waterLevel": 57,
	"tankName": "Tank 16",
	"tankShape": "Cylindrical",
	"observationDateTime": "2021-03-11T15:51:02+05:30",
	"compensatedTDS":25,
	"uncompensatedTDS":27
}

normalizedPayload = {
    "id": "urn:ngsi-ld:AttributeProperty:a3003",
    "type": "AttributeProperty",
    "language": {
        "type": "Property",
        "value": [
            "en",
            "fr"
        ]
    },
    "label": {
        "type": "Property",
        "value": {
            "en": "SDMX attribute COMMENT_OBS",
            "fr": "Attribut SDMX "
        }
    },
    "concept": {
        "type": "Relationship",
        "value": "urn:ngsi-ld:Concept:c4303"
    },
    "created": {
        "type": "Property",
        "value": "2022-01-15T07:00:00+00:00"
    },
    "identifier": {
        "type": "Property",
        "value": "a3003"
    },
    "modified": {
        "type": "Property",
        "value": "2022-01-15T07:30:00+00:00"
    },
    "range": {
        "type": "Property",
        "value": "xsd:string"
    },
    "@context": [
        "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}

payload = normalized2keyvalues(normalizedPayload)
print(payload)
with open("example-normalized.json", "w") as file:
    json.dump(payload, file)

# schema = keyvalues2normalized(keyvaluesPayload)
# with open("keyvalues.json", "w") as file:
#     json.dump(schema, file)
