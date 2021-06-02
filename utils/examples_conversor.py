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
  "id": "Vulnerability.01",
  "type": "Vulnerability",
  "analyzedAt": "2020-12-24T12:00:00Z",
  "analysisType": "Flood Vulnerability Maps",
  "location": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          23.6627,
          41.88768
        ],
        [
          25.85598,
          43.38622
        ],
        [
          23.4899,
          43.78691
        ],
        [
          22.35609,
          42.28869
        ],
        [
          23.6627,
          41.88769
        ]
      ]
    ]
  },
  "vulnerabilityValues": [
    1,
    2,
    3
  ],
  "contentInformation": [
    {
      "id": 0,
      "value": "Low",
      "color": "(170, 255, 0)"
    },
    {
      "id": 1,
      "value": "Medium",
      "color": "(255, 255, 0)"
    },
    {
      "id": 2,
      "value": "High",
      "color": "(255, 170, 0)"
    }
  ],
  "createsLayers": [
    "EOGeoDataLayer.01",
    "EOGeoDataLayer.02"
  ]
}
"""


normalizedPayload = """
{
  "id": "urn:ngsi-ld:RegulationStructure:id:IXHN:40075061",
  "type": "RegulationStructure",
  "location": {
    "type": "Property",
    "value": {
      "type": "Point",
      "coordinates": [
        -72.3447045,
        44.679442
      ]
    }
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "",
      "addressLocality": "",
      "addressRegion": "",
      "addressCountry": "",
      "postalCode": "",
      "postOfficeBoxNumber": "",
      "areaServed": ""
    }
  },
  "areaServed": {
    "type": "Property",
    "value": ""
  },
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "1986-07-26T02:43:28Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2021-03-21T17:56:26Z"
    }
  },
  "source": {
    "type": "Property",
    "value": ""
  },
  "name": {
    "type": "Property",
    "value": "RS01"
  },
  "alternateName": {
    "type": "Property",
    "value": "RS01 Thivae"
  },
  "description": {
    "type": "Property",
    "value": "Regulation Structure Thivae"
  },
  "dataProvider": {
    "type": "Property",
    "value": "EYDAP"
  },
  "owner": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:RegulationStructure:items:ASWJ:21246595",
      "urn:ngsi-ld:RegulationStructure:items:NHFZ:56673870"
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:RegulationStructure:items:PLEL:78574823",
      "urn:ngsi-ld:RegulationStructure:items:IZVF:62633698"
    ]
  },
  "tag": {
    "type": "Property",
    "value": ""
  },
  "numberOfGates": {
    "type": "Property",
    "value": 2
  },
  "numberOfSpillways": {
    "type": "Property",
    "value": 2
  },
  "teleCommand": {
    "type": "Property",
    "value": [
      "true"
    ]
  },
  "hasSluiceGate": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:RegulationStructure:hasSluiceGate:JXFD:60487647"
  },
  "hasSpillway": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:RegulationStructure:hasSpillway:CBWI:21948924"
  },
  "position": {
    "type": "Property",
    "value": {
      "distance": 864.6,
      "refPoint": "urn:ngsi-ld:RegulationStructure:refPoint:JXFD:60487647"
    }
  },
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}

"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
