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
        rawoutput = json.dumps(output, indent=2)
        outputfile.write(rawoutput)
    return output


keyvaluesPayload ={
  "_id": "6557985a8f4f3ce5fd4e87df",
  "id": "https://smartdatamodels.org/dataModel.Hl7/Account/_valueDate/extension#0.0.1",
  "parentContext": "https://smartdatamodels.org/dataModel.Hl7/_valueDate",
  "parentId": "https://smartdatamodels.org/dataModel.Hl7/Account/_valueDate#0.0.1",
  "context": "https://smartdatamodels.org/dataModel.Hl7/extension",
  "property": "extension",
  "dataModel": "Account",
  "repoName": "dataModel.Hl7",
  "modelTags": "HL7",
  "license": "https://github.com/smart-data-models/dataModel.Hl7/blob/master/Account/LICENSE.md",
  "schemaVersion": "0.0.1",
  "dataType": "array",
  "description": "May be used to represent additional information that is not part of the basic definition of the element. To make the use of extensions safe and manageable, there is a strict set of governance  applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension"
}


normalizedPayload = {
  "id": "urn:ngsi-ld:InteroperableAssets:id:WGEQ:22085426",
  "type": "InteroperableAssets",
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2024-04-22T01:37:25Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2024-04-24T17:29:14Z"
    }
  },
  "source": {
    "type": "Property",
    "value": "Sm4rtenance Project"
  },
  "name": {
    "type": "Property",
    "value": ""
  },
  "alternateName": {
    "type": "Property",
    "value": ""
  },
  "description": {
    "type": "Property",
    "value": ""
  },
  "dataProvider": {
    "type": "Property",
    "value": ""
  },
  "owner": {
    "type": "Property",
    "value": [
      ""
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      ""
    ]
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        40.41,
        3.7033
      ]
    }
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "",
      "addressLocality": "Madrid",
      "addressRegion": "Madrid",
      "addressCountry": "Spain",
      "postalCode": "28050",
      "postOfficeBoxNumber": "",
      "streetNr": "",
      "district": ""
    }
  },
  "areaServed": {
    "type": "Property",
    "value": ""
  },
  "dataSpaceIdentifier": {
    "type": "Property",
    "value": "SM4RTENANCE"
  },
  "dataExchangeProtocols": {
    "type": "Property",
    "value": [
      {
        "name": "Link Data event stream",
        "description": "A Linked Data Event Stream (LDES) is a technical standard that applies linked data principles to data streams, allowing for the exchange of data between silos in a sustainable and cost-effective manner. It is defined as a collection of immutable objects, called LDES members, described using the Resource Description Framework (RDF). LDES enables data publishers to publish their datasets as append-only collections, allowing consumers to replicate the full dataset and keep it synchronized, while also facilitating real-time updates and improving data usability and findability",
        "identifier": "LDES",
        "version": "1.0",
        "documentation": [
          "https://semiceu.github.io/LinkedDataEventStreams/"
        ]
      },
      {
        "name": "NGSI LD",
        "description": "NGSI-LD is an information model and API for publishing, querying, and subscribing to context information, standardized by ETSI to facilitate open exchange and sharing of structured data across various domains. It represents context information as entities with properties and relationships, using a property graph model with semantics based on RDF and the semantic web framework. NGSI-LD builds upon previous context management frameworks and can be serialized using JSON-LD, making it compatible with linked data principles and allowing for unique IRI identifiers for entities and relationships",
        "identifier": "NGSI-LD.1.6",
        "version": "1.6",
        "documentation": [
          "https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.06.01_60/gs_CIM009v010601p.pdf"
        ]
      }
    ]
  },
  "dataModelSources": {
    "type": "Property",
    "value": [
      {
        "name": "Smart Data Models",
        "description": "The Smart Data Models initiative is a collaborative effort led by FIWARE Foundation, TM Forum, IUDX, and OASC to create and promote standardized, interoperable data models across multiple sectors. It aims to support a digital marketplace of smart solutions by developing common, royalty-free data models that are publicly available. The initiative focuses on using JSON Schema as a core component, enabling exports in various formats to enhance compatibility with semantic and linked data approaches. By providing these open-licensed, standardized data models, the initiative seeks to combat data silos, improve data sharing, and facilitate application portability across different platforms and sectors, ultimately fostering innovation and interoperability in smart solutions.",
        "identifier": "Smart-Data-Models",
        "internalIdentifier": "WeatherObserved",
        "version": "0.3",
        "documentation": [
          "https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/doc/spec.md"
        ]
      }
    ]
  },
  "@context": [
    "https://smart-data-models.github.io/dataModel.DataSpace/context.jsonld"
  ]
}






payload = normalized2keyvalues(normalizedPayload)
# print(payload)
with open("keyvalues.json", "w") as file:
    json.dump(payload, file, indent=2)

# schema = keyvalues2normalized(keyvaluesPayload)
# with open("example-normalized.json", "w") as file:
#     json.dump(schema, file, indent=2)
