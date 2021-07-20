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
  "id": "uri:ngsi-ld:datapackage:001",
  "type": "DataPackageFrictionlessData",
  "name": "cpi",
  "title": "Annual Consumer Price Index (CPI)",
  "description": "Annual Consumer Price Index (CPI) for most countries in the world. Reference year is 2005.",
  "profile": "tabular-data-package",
  "licenses": [
    {
      "name": "CC-BY-4.0",
      "title": "Creative Commons Attribution 4.0",
      "path": "https://creativecommons.org/licenses/by/4.0/"
    }
  ],
  "keywords": [
    "CPI",
    "World",
    "Consumer Price Index",
    "Annual Data",
    "The World Bank"
  ],
  "version": "2.0.0",
  "sources": [
    {
      "title": "The World Bank",
      "path": "http://data.worldbank.org/indicator/FP.CPI.TOTL"
    }
  ],
  "resources": [
    {
      "path": "data/cpi.csv",
      "name": "cpi",
      "profile": "tabular-data-resource",
      "schema": {
        "fields": [
          {
            "name": "Country Name",
            "type": "string"
          },
          {
            "name": "Country Code",
            "type": "string"
          },
          {
            "name": "Year",
            "type": "year"
          },
          {
            "name": "CPI",
            "description": "CPI (where 2005=100)",
            "type": "number"
          }
        ]
      }
    }
  ],
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}
"""


normalizedPayload = """{
  "id": "urn:ngsi-ld:DistributionDCAT-AP:id:NUZE:76215118",
  "dateCreated": {
    "type": "DateTime",
    "value": "1993-08-16T05:35:56Z"
  },
  "dateModified": {
    "type": "DateTime",
    "value": "1970-07-14T10:48:19Z"
  },
  "source": {
    "type": "Text",
    "value": ""
  },
  "name": {
    "type": "Text",
    "value": "csv portals distribution"
  },
  "alternateName": {
    "type": "Text",
    "value": "csv"
  },
  "description": {
    "type": "Text",
    "value": "Distribution of open data portals in csv"
  },
  "dataProvider": {
    "type": "Text",
    "value": "Meloda.org"
  },
  "owner": {
    "type": "Text",
    "value": [
      "urn:ngsi-ld:DistributionDCAT-AP:items:HZAC:24935175",
      "urn:ngsi-ld:DistributionDCAT-AP:items:AQGQ:50019342"
    ]
  },
  "seeAlso": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:DistributionDCAT-AP:items:TYQY:03354957",
      "urn:ngsi-ld:DistributionDCAT-AP:items:VZQW:12690544"
    ]
  },
  "location": {
    "type": "geo:json",
    "value": {
      "type": "Point",
      "coordinates": [
        -67.057831,
        67.968509
      ]
    }
  },
  "address": {
    "type": "PostalAddress",
    "value": {
      "streetAddress": "Luxembourg platz 2",
      "addressLocality": "Luxembourg",
      "addressRegion": "Luxembourg",
      "addressCountry": "Luxembourg",
      "postalCode": "24004",
      "postOfficeBoxNumber": ""
    }
  },
  "areaServed": {
    "type": "Text",
    "value": "European Union."
  },
  "accessUrl": {
    "type": "array",
    "value": [
      ""
    ]
  },
  "availability": {
    "type": "Text",
    "value": "yes"
  },
  "format": {
    "type": "Text",
    "value": " text/csv"
  },
  "license": {
    "type": "Text",
    "value": "CC-BY"
  },
  "accessService": {
    "type": "array",
    "value": [
      ""
    ]
  },
  "byteSize": {
    "type": "array",
    "value": 43503
  },
  "checksum": {
    "type": "Text",
    "value": "H3FR."
  },
  "compressionFormat": {
    "type": "Text",
    "value": ""
  },
  "documentation": {
    "type": "array",
    "value": [
    ]
  },
  "downloadURL": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:DistributionDCAT-AP:items:HVWX:12201868",
      "urn:ngsi-ld:DistributionDCAT-AP:items:ICPI:96947751"
    ]
  },
  "hasPolicy": {
    "type": "Text",
    "value": "Open data policy."
  },
  "language": {
    "type": "array",
    "value": [
      "EN",
      "ES"
    ]
  },
  "linkedSchemas": {
    "type": "array",
    "value": [
    ]
  },
  "mediaType": {
    "type": "Text",
    "value": ""
  },
  "packagingFormat": {
    "type": "Text",
    "value": "zip"
  },
  "releaseDate": {
    "type": "DateTime",
    "value": "1997-05-06T05:04:10Z"
  },
  "rights": {
    "type": "Text",
    "value": "copyleft"
  },
  "spatialResolution": {
    "type": "array",
    "value": [
      0.5,
      0.5
    ]
  },
  "status": {
    "type": "Text",
    "value": "Withdrawn"
  },
  "temporalResolution": {
    "type": "array",
    "value": [
      2,
      10
    ]
  },
  "title": {
    "type": "array",
    "value": [
      "Dataset base"
    ]
  },
  "modifiedDate": {
    "type": "DateTime",
    "value": "1986-03-28T19:56:43Z"
  }
}

"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
