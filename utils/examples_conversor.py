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
  "id": "urn:ngsi-ld:CatalogueRecordDCAT-AP:id:KFTL:88140679",
  "dateCreated": "2020-11-02T21:25:54Z",
  "dateModified": "2021-07-02T18:37:55Z",
  "source": "",
  "name": "",
  "alternateName": "",
  "description": "Catalogue record of the solar system open data portal",
  "dataProvider": "european open data portal",
  "owner": [
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:ISXP:07320625",
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:BQMW:23610768"
  ],
  "seeAlso": [
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:FVCU:03753474",
    "urn:ngsi-ld:CatalogueRecordDCAT-AP:items:AIEC:73224831"
  ],
  "location": {
    "type": "Point",
    "coordinates": [
      36.633152,
      -85.183315
    ]
  },
  "address": {
    "streetAddress": "2, rue Mercier",
    "addressLocality": "Luxembourg",
    "addressRegion": "Luxembourg",
    "addressCountry": "Luxembourg",
    "postalCode": "2985",
    "postOfficeBoxNumber": ""
  },
  "areaServed": "European Union and beyond",
  "type": "CatalogueRecordDCAT-AP",
  "primaryTopic": "Public administration",
  "modificationDate": "2021-07-02T18:37:55Z",
  "applicationProfile": "DCAT Application profile for data portals in Europe",
  "changeType": "First version",
  "listingDate": "2021-07-02T18:37:55Z",
  "language": [
    "EN",
    "ES"
  ],
  "sourceMetadata": "",
  "title": [
    "Example of catalogue record",
    "Ejemplo de registro de catálogo"
  ]
}
"""


normalizedPayload = """
{
  "id": "urn:ngsi-ld:CSVDialect:id:OAPS:03889914",
  "type": "Missing entity name",
  "dateCreated": {
    "type": "DateTime",
    "value": "1986-03-01T17:11:28Z"
  },
  "dateModified": {
    "type": "DateTime",
    "value": "2017-04-29T03:29:41Z"
  },
  "source": {
    "type": "Text",
    "value": ""
  },
  "name": {
    "type": "Text",
    "value": ""
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
      "urn:ngsi-ld:CSVDialect:items:YPBX:70706198",
      "urn:ngsi-ld:CSVDialect:items:MABG:25535507"
    ]
  },
  "seeAlso": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:CSVDialect:items:YNLD:15120048",
      "urn:ngsi-ld:CSVDialect:items:EFIZ:80683325"
    ]
  },
  "csvddfVersion": {
    "type": "number",
    "value": 1.2
  },
  "delimiter": {
    "type": "Text",
    "value": ";"
  },
  "doubleQuote": {
    "type": "boolean",
    "value": true
  },
  "lineTerminator": {
    "type": "Text",
    "value": "\\r\\n"
  },
  "nullSequence": {
    "type": "Text",
    "value": "\\N"
  },
  "quoteChar": {
    "type": "Text",
    "value": "'"
  },
  "escapeChar": {
    "type": "Text",
    "value": "\\\\"
  },
  "skipInitialSpace": {
    "type": "boolean",
    "value": false
  },
  "header": {
    "type": "boolean",
    "value": false
  },
  "commentChar": {
    "type": "Text",
    "value": "#"
  },
  "caseSensitiveHeader": {
    "type": "boolean",
    "value": true
  }
}



"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
