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

    print(output)
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
  "id": "urn:ngsi-ld:QueueMonitor:id:SIHJ:22618237",
  "type": "QueueMonitor",
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2021-03-22T11:10:04Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2021-03-22T11:10:05Z"
    }
  },
  "source": {
    "type": "Property",
    "value": ""
  },
  "name": {
    "type": "Property",
    "value": "Queue system of the tourist attraction of Leon Cathedral"
  },
  "alternateName": {
    "type": "Property",
    "value": "Cathedral queue"
  },
  "description": {
    "type": "Property",
    "value": "Queue system of the tourist attraction of Leon Cathedral for allowing a limited visitors inside the building"
  },
  "dataProvider": {
    "type": "Property",
    "value": ""
  },
  "owner": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:QueueMonitor:items:TLDV:47467690",
      "urn:ngsi-ld:QueueMonitor:items:JTAO:46330396"
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:QueueMonitor:items:SHMV:05050086",
      "urn:ngsi-ld:QueueMonitor:items:QQJP:06476874"
    ]
  },
  "location": {
    "type": "Property",
    "value": {
      "type": "Point",
      "coordinates": [
        42.605556,
        -5.57
      ]
    }
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "Plaza de la Catedrla s/n",
      "addressLocality": "León",
      "addressRegion": "Castilla y León",
      "addressCountry": "Spain",
      "postalCode": "24001",
      "postOfficeBoxNumber": "",
      "areaServed": "City Center."
    }
  },
  "areaServed": {
    "type": "Property",
    "value": "City Center"
  },
  "localId": {
    "type": "Property",
    "value": "system-1"
  },
  "officeName": {
    "type": "Property",
    "value": "Tourist Office"
  },
  "serviceName": {
    "type": "Property",
    "value": "Visit reservations."
  },
  "serviceId": {
    "type": "Property",
    "value": "Cathedral-reservations-visit-1"
  },
  "serviceStatus": {
    "type": "Property",
    "value": "Open"
  },
  "serviceStatusNote": {
    "type": "Property",
    "value": ""
  },
  "scheduleTime": {
    "type": "Property",
    "value": "2021-02-21T12:47:04Z"
  },
  "queueLine": {
    "type": "Property",
    "value": "Groups line."
  },
  "linePriority": {
    "type": "Property",
    "value": 1
  },
  "lastTicketIssued": {
    "type": "Property",
    "value": 33
  },
  "lastTicketIssuedLabel": {
    "type": "Property",
    "value": "C-33"
  },
  "ticketServed": {
    "type": "Property",
    "value": 45
  },
  "ticketServedLabel": {
    "type": "Property",
    "value": "C-45"
  },
  "ticketsToServe": {
    "type": "Property",
    "value": 12
  },
  "@context": [
    "https://smart-data-models.github.io/data-models/context.jsonld"
  ]
}
    """

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
