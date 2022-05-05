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

    print(output)
    return output





keyvaluesPayload = {
  "id": "urn:ngsi-ld:AnimalDisease:ca3f1295-500c-4aa3-b745-d143097d5c01",
  "type": "AnimalDisease",
  "disease": "Lameness",
  "diagnosticTest": "Visual inspection",
  "date": "2022-01-01T01:20:00Z",
  "animals": [
    "urn:ngsi-ld:Animal:ca3f1295-500c-4aa3-b745-d143097d5c01",
    "urn:ngsi-ld:Animal:bb3f1295-500c-4aa3-b745-d143097d4321"
  ],
  "veterinarianTreatment": "urn:ngsi-ld:VeterinarianTreatment:ca3f1295-500c-4aa3-b745-d143097d5c65",
  "veterinarian": "urn:ngsi-ld:Veterinarian:ca3f1295-500c-4aa3-b745-d143097d5d11",
  "@context": [
    "https://smart-data-models.github.io/dataModel.Agrifood/context.jsonld"
  ]
}



normalizedPayload = """
{
  "id": "urn:ngsi-ld:Sump:1",
  "type": "Sump",
  "totalGasPressure": {
    "type": "Property",
    "value": 1,
    "unitCode": "Pa",
    "observedAt": "2020-06-26T21:32:52Z",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:02"
    }
  },
  "redoxPotential": {
    "type": "Property",
    "value": 80,
    "unitCode": "2Z",
    "observedAt": "2020-06-26T21:32:52Z",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:02"
    }
  },
  "co2": {
    "type": "Property",
    "value": 7,
    "unitCode": "59",
    "observedAt": "2020-06-26T21:32:52Z",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:02"
    }
  },
  "pH": {
    "type": "Property",
    "value": 7,
    "unitCode": "Q30",
    "observedAt": "2020-06-26T21:32:52Z",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:02"
    }
  },
  "waterConsumption": {
    "type": "Property",
    "value": 10,
    "unitCode": "LTR",
    "observedAt": "2020-06-26T21:32:52Z",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:02"
    }
  },
  "refFishContainement": [
    {
      "type": "Relationship",
      "object": "urn:ngsi-ld:FishContainment:01",
      "datasetId": "urn:ngsi-ld:Dataset:FishContainment:01"
    },
    {
      "type": "Relationship",
      "object": "urn:ngsi-ld:FishContainment:02",
      "datasetId": "urn:ngsi-ld:Dataset:FishContainment:02"
    }
  ],
  "processes": {
    "type": "Property",
    "value": [
      "O3 cone",
      "02 cone",
      "UV filter"
    ]
  },
  "@context": [
    "https://raw.githubusercontent.com/smart-data-models/data-models/master/context.jsonld"
  ]
}
"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
