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
  "id": "02ce3860-3126-42af-8ac7-c2a661134130",
  "type": "Berth",
  "mrn": "urn:mrn:eshuv:portcalls:berth:id:18013",
  "gln": 1234567890123,
  "portCode": "ESHUV",
  "year": 2023,
  "portCallNumber": "ESHUV202300123",
  "portCallRef": "urn:mrn:eshuv:portcalls:portcall:2023:id:941",
  "stopRank": 2,
  "terminal": "Muelle Levante",
  "berthCode": "urn:mrn:eshuv:portcalls:berth:code:10",
  "berthName": "Levante comercial",
  "gln": 84332157000139,
  "firstBollard": "N03",
  "lastBollard": "N12",
  "status": "AUTHORIZED",
  "requestedAt": "2023-01-01T07:30:00",
  "authorizedAt": "2023-01-01T07:30:00",
  "berthingTypeCode": "AB1",
  "mooringLines": 12,
  "activityCode": "ZOP",
  "etaBerth": "2023-01-01T07:30:00",
  "rtaBerth": "2023-01-01T07:30:00",
  "ptaBerth": "2023-01-01T07:30:00",
  "ataBerth": "2023-01-01T07:30:00",
  "etdBerth": "2023-01-01T07:30:00",
  "rtdBerth": "2023-01-01T07:30:00",
  "ptdBerth": "2023-01-01T07:30:00",
  "atdBerth": "2023-01-01T07:30:00",
  "arrivalDraught": 12.3,
  "departureDraught": 9.5,
  "remarks": "FONDEA PARA SUMINISTRO DE COMBUSTIBLE POR GABARRA",
  "authorizationRemarks": "authorized after departure of ship XX",
  "agentName": "Acme Huelva S.L.",
  "agentLegalCode": "A-98345678",
  "createdAt": "2023-01-01T07:30:00",
  "modifiedAt": "2023-01-01T07:30:00"
}

normalizedPayload ={
  "id": "urn:ngsi-ld:Memory:id:XJWG:82694953",
  "type": "Memory",
  "dateCreated": {
    "type": "Date-Time",
    "value": "2024-02-12T22:38:51Z"
  },
  "dateModified": {
    "type": "Date-Time",
    "value": "2024-04-02T15:33:47Z"
  },
  "source": {
    "type": "Text",
    "value": ""
  },
  "name": {
    "type": "Text",
    "value": "regular memory"
  },
  "alternateName": {
    "type": "Text",
    "value": ""
  },
  "description": {
    "type": "Text",
    "value": ""
  },
  "dataProvider": {
    "type": "Text",
    "value": ""
  },
  "owner": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:Memory:items:HIOM:43953773"
    ]
  },
  "seeAlso": {
    "type": "array",
    "value": [
    ]
  },
  "location": {
    "type": "geo:json",
    "value": {
      "type": "Point",
      "coordinates": [
        50.8484048,
        4.3671841
      ]
    }
  },
  "address": {
    "type": "StructuredValue",
    "value": {
      "streetAddress": "Avenue des Arts",
      "addressLocality": "Brussels",
      "addressRegion": "Stay ",
      "addressCountry": "Belgium",
      "postalCode": "1210",
      "postOfficeBoxNumber": "",
      "streetNr": "6-9",
      "district": ""
    }
  },
  "areaServed": {
    "type": "Text",
    "value": "europe"
  },
  "memorySize": {
    "type": "Number",
    "value": 16,
    "unitCode": "Gb"
  },
  "memoryClass": {
    "type": "Text",
    "value": "DDR SDRAM"
  },
  "memoryRank": {
    "type": "Text",
    "value": "other"
  },
  "eccEnabled": {
    "type": "Boolean",
    "value": False
  },
  "hardwareEncryption": {
    "type": "Boolean",
    "value": False
  }
}





# payload = normalized2keyvalues(normalizedPayload)
# # print(payload)
# with open("keyvalues.json", "w") as file:
#     json.dump(payload, file, indent=2)

schema = keyvalues2normalized(keyvaluesPayload)
with open("example-normalized.json", "w") as file:
    json.dump(schema, file, indent=2)
