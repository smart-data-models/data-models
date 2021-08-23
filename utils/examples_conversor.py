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
  "id": "urn:ngsi-ld:TableSchemaFrictionlessData:XVFE:0034",
  "type": "TableSchemaFrictionlessData",
  "fields": [
    {
      "name": "first_name",
      "type": "string",
      "constraints": {
        "required": true
      }
    },
    {
      "name": "age",
      "type": "integer"
    }
  ],
  "primaryKey": [
    "name"
  ]
}
"""


normalizedPayload = """
{
  "id": "urn:ngsi-ld:FareCollectionSystem:id:RJSB:34513580",
  "type": "FareCollectionSystem",
  "dateCreated": {
    "type": "DateTime",
    "value": "2020-11-02T06:16:42Z"
  },
  "dateModified": {
    "type": "DateTime",
    "value": "2020-12-27T15:13:17Z"
  },
  "source": {
    "type": "Text",
    "value": ""
  },
  "name": {
    "type": "Text",
    "value": "Fare collection system Nize"
  },
  "alternateName": {
    "type": "Text",
    "value": ""
  },
  "description": {
    "type": "Text",
    "value": "Fare collection system Nize for regional routes"
  },
  "dataProvider": {
    "type": "Text",
    "value": ""
  },
  "owner": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:FareCollectionSystem:items:XMXR:79897582",
      "urn:ngsi-ld:FareCollectionSystem:items:SKAX:98192518"
    ]
  },
  "seeAlso": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:FareCollectionSystem:items:VSVS:72352464",
      "urn:ngsi-ld:FareCollectionSystem:items:VMFR:36424993"
    ]
  },
  "location": {
    "type": "geo:json",
    "value": {
      "type": "Point",
      "coordinates": [
        43.7034,
        7.2663
      ]
    }
  },
  "address": {
    "type": "PostalAddress",
    "value": {
      "streetAddress": "Av. Nicolas II",
      "addressLocality": "Nice",
      "addressRegion": "Provenza-Alpes-Costa Azul",
      "addressCountry": "France",
      "postalCode": "06000",
      "postOfficeBoxNumber": ""
    }
  },
  "areaServed": {
    "type": "Text",
    "value": "Nice"
  },
  "destinationStopName": {
    "type": "Text",
    "value": "Hour risk somebody deal system discussion other plan. Stage the film occur."
  },
  "occupancyLevel": {
    "type": "Text",
    "value": "Green"
  },
  "travelDistance": {
    "type": "number",
    "value": 7.5
  },
  "passengerCount": {
    "type": "number",
    "value": 6
  },
  "transactionType": {
    "type": "Text",
    "value": "Issue"
  },
  "ticketTypeCode": {
    "type": "Text",
    "value": "Normal"
  },
  "originStopName": {
    "type": "Text",
    "value": "Vauban"
  },
  "entryAreaCode": {
    "type": "Text",
    "value": "city-bus-service"
  },
  "cardId": {
    "type": "Text",
    "value": "987201910"
  },
  "transactionTypeId": {
    "type": "Text",
    "value": "2401"
  },
  "stage": {
    "type": "number",
    "value": 4
  },
  "equipmentId": {
    "type": "Text",
    "value": "S23"
  },
  "direction_id": {
    "type": "number",
    "value": 1
  },
  "equipmentSequenceNumber": {
    "type": "number",
    "value": 2
  },
  "shiftOfOperation": {
    "type": "Text",
    "value": "2"
  },
  "route_id": {
    "type": "Text",
    "value": "4"
  },
  "trip_id": {
    "type": "Text",
    "value": "4A"
  },
  "originStopCategory": {
    "type": "Text",
    "value": "Bus stop"
  },
  "vehicle_label": {
    "type": "Text",
    "value": "5821JZS"
  },
  "fareForChild": {
    "type": "number",
    "value": 3.6
  },
  "transactionDateTime": {
    "type": "DateTime",
    "value":  "2021-08-20T15:45:22Z"
    
  },
  "destinationStopId": {
    "type": "Text",
    "value": "Nice-Airport"
  },
  "originDestinationCode": {
    "type": "Text",
    "value": "23"
  },
  "currentTripCount": {
    "type": "number",
    "value": 12
  },
  "equipmentTypeCode": {
    "type": "Text",
    "value": "42"
  },
  "destinationStopCategory": {
    "type": "Text",
    "value": "Airport"
  },
  "transactionVehicleNum": {
    "type": "number",
    "value": 23
  },
  "fareForAdult": {
    "type": "number",
    "value": 4.5
  },
  "observationDateTime": {
    "type": "DateTime",
    "value": "1988-12-24T07:06:19Z"
  },
  "equipmentCompanyCode": {
    "type": "Text",
    "value": "103"
  },
  "transactionTypeDescription": {
    "type": "Text",
    "value": "Regular Fare."
  },
  "exitAreaCode": {
    "type": "Text",
    "value": "city-bus-service"
  },
  "equipmentType": {
    "type": "Text",
    "value": "Entry sensor"
  },
  "equipmentStopId": {
    "type": "Text",
    "value": "BRTS-Sen-23"
  },
  "originStopId": {
    "type": "Text",
    "value": "9"
  },
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}

"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
