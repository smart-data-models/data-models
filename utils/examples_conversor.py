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
  "id": "0.E.6.AY1.A1",
  "type": "Action",
  "refProject": "O.E.6.AY1",
  "dateCreated": "2016-08-08T10:18:16Z",
  "dateModified": "2016-08-08T10:18:16Z",
  "name": "Realizacion de campafias de promoci6n en medios de comunicaci6n de la provincia",
  "executionPeriod": "2021S1",
  "compliancePercentage": 0,
  "modifications": "SIN MODIFICACION"
}


normalizedPayload = {
  "id": "urn:ngsi-ld:Catalogue:id:KSLT:97146192",
  "type": "Catalogue",
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2023-03-20T18:53:50Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2023-06-29T11:37:12Z"
    }
  },
  "source": {
    "type": "Property",
    "value": "INE"
  },
  "name": {
    "type": "Property",
    "value": "Catalogue of statistical resources"
  },
  "alternateName": {
    "type": "Property",
    "value": "Catalogue"
  },
  "description": {
    "type": "Property",
    "value": "List of converted statistical resources"
  },
  "dataProvider": {
    "type": "Property",
    "value": "INE"
  },
  "owner": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:Catalogue:items:FRAY:12902985",
      "urn:ngsi-ld:Catalogue:items:WMSS:90165917"
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:Catalogue:items:XSHA:97687196"
    ]
  },
  "location": {
    "type": "Property",
    "value": {
      "type": "Point",
      "coordinates": [
        52.5209531,
        13.3256918
      ]
    }
  },
  "address": {
    "streetAddress": "Franklinstrasse 13",
    "addressLocality": "Berlin",
    "addressRegion": "Berlin",
    "addressCountry": "Germany",
    "postalCode": "10587",
    "postOfficeBoxNumber": "",
    "streetNr": "13",
    "district": ""
  },
  "areaServed": "",
  "dataset": {
    "type": "object",
    "value": "urn:ngsi-ld:Catalogue:dataset:VLNR:72960176"
  },
  "publisher": {
    "type": "Property",
    "value": "INE"
  },
  "title": {
    "type": "Property",
    "value": [
      "Catalogue or statistical resources",
      "Catálogo de recursos estadisticos"
    ]
  },
  "homepage": {
    "type": "Property",
    "value": "urn:ngsi-ld:Catalogue:homepage:FXWI:96370263"
  },
  "language": {
    "type": "Property",
    "value": [
      "SP",
      "EN"
    ]
  },
  "licence": {
    "type": "Property",
    "value": "CC BY 4.0"
  },
  "releaseDate": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2023-01-20T11:03:48Z"
    }
  },
  "themes": {
    "type": "Property",
    "value": [
      "demography",
      "social movements"
    ]
  },
  "modificationDate": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2023-02-24T16:28:58Z"
    }
  },
  "hasPart": {
    "type": "object",
    "value": "urn:ngsi-ld:Catalogue:hasPart:EQFC:38298320"
  },
  "isPartOf": {
    "type": "object",
    "value": "urn:ngsi-ld:Catalogue:isPartOf:JACJ:87819283"
  },
  "record": {
    "type": "object",
    "value": "urn:ngsi-ld:Catalogue:record:UEFV:49174271"
  },
  "rights": {
    "type": "Property",
    "value": "Open licensed"
  },
  "spatial_geographic": {
    "type": "Property",
    "value": [
      {
        "type": "Point",
        "coordinates": [
          121.7,
          146.6
        ],
        "bbox": [
          46.5,
          926.8,
          995.6,
          403.5
        ]
      },
      {
        "type": "Point",
        "coordinates": [
          60.3,
          491.9
        ],
        "bbox": [
          652.6,
          335.8,
          341.6,
          875.0
        ]
      }
    ]
  },
  "@context": [
    "https://raw.githubusercontent.com/smart-data-models/dataModel.STAT-DCAT-AP/master/context.jsonld"
  ]
}



payload = normalized2keyvalues(normalizedPayload)
print(payload)
with open("example-normalized.json", "w") as file:
    json.dump(payload, file)

# schema = keyvalues2normalized(keyvaluesPayload)
# with open("keyvalues.json", "w") as file:
#     json.dump(schema, file)
