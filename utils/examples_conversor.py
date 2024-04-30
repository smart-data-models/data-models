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
  "id": "$af4345f234525$",
  "mrn": "urn:mrn:eshuv:portcalls:portcall:id:941",
  "type": "PortCall",
  "portCode": "ESVLC",
  "portCallNumber": "ESHUV202301296",
  "regularLine": "BALE: CITY1 - ISLANDER",
  "terminal": "TERMINAL ESTE, S.A.",
  "status": "AUTHORIZED",
  "authorizedBy": "PORT_ARMY_AUTHORITIES",
  "authorizationDate": "2023-01-01T08:00:00.00Z",
  "voyageNumber": "12021060223",
  "lastPortCode": "ESBCN",
  "nextPortCode": "NLRTM",
  "vesselTypeCategory": "CONTAINER",
  "vesselTypeClass": "FULL CONTAINER",
  "vesselRef": "URI:NGSI-LD:Portcall:001",
  "vesselMrn": "urn:mrn:ESHUV:portcalls:portcallvessel:id:12345",
  "vesselName": "Acme ERC SHIP",
  "imo": 87123445,
  "mmsi": 210049000,
  "callSign": "5BP-*987C3",
  "masterName": "John Doe",
  "wasteAgreementExists": True,
  "dangerousGoodsCarried": True,
  "dangerousGoodsLoading": True,
  "dangerousGoodsUnloading": False,
  "agentName": "Acme Consignors S.L.",
  "agentLegalCode": "A-43242342",
  "agentChangeDate": "2023-01-01T08:00:00",
  "secondAgentName": "John Doe",
  "secondAgentLegalCode": "31133133-V",
  "manifestActivated": True,
  "manifestActivationDate": "2023-01-01T08:00:00",
  "interiorTraffic": False,
  "remarks": "Fondeado hasta arreglar avería",
  "crewArrival": 100,
  "crewDeparture": 120,
  "passengersArrival": 20,
  "passengersDeparture": 25,
  "eta": "2023-01-01T07:15:00",
  "rta": "2023-01-01T07:30:00",
  "pta": "2023-01-01T07:15:00",
  "ata": "2023-01-01T08:00:00",
  "etd": "2023-01-02T07:15:00",
  "rtd": "2023-01-02T07:00:00",
  "ptd": "2023-01-02T07:00:00",
  "atd": "2023-01-02T07:00:00",
  "regularLine": "GRIMALDI - SHORT SEA SERVICE B",
  "@context": [
    "https://raw.githubusercontent.com/smart-data-models/dataModel.MarineTransport/master/context.jsonld"
  ]
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





payload = normalized2keyvalues(normalizedPayload)
# print(payload)
with open("keyvalues.json", "w") as file:
    json.dump(payload, file, indent=2)

# schema = keyvalues2normalized(keyvaluesPayload)
# with open("example-normalized.json", "w") as file:
#     json.dump(schema, file, indent=2)
