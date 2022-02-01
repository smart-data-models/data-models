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





keyvaluesPayload = """
{
  "id": "https://smart-data-models.github.io/SmartCities/RevenueCollection/schema.json",
  "type": "RevenueCollection",
  "totalCount": 436,
  "registrationCertificateRecoveryAmount": 10400,
  "enrollmentCertificateRecoveryAmount": 8400,
  "year": "2020",
  "dateObserved": "2021-11-10T01:16:01Z",
  "month": "02",
  "revenueCollectionType": "Property Tax",
  "vehicleTypeCode": "2",
  "amountCollected": 20400,
  "vehicleType": "motorcycle",
  "municipalityInfo": {
    "district": "Bangalore Urban",
    "ulbName": "BMC",
    "cityID": "23",
    "stateName": "Karnataka",
    "cityName": "Bangalore",
    "zoneID": "2",
    "wardNum": 4
  }
}
"""


normalizedPayload = """
{
  "@context": {
    "isc": "http://id.cef-interstat.eu/sc/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "qb": "http://purl.org/linked-data/cube#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "sdmp": "https://...",
    "sdmx-attribute": "http://purl.org/linked-data/sdmx/2009/attribute#",
    "sdmx-concept": "http://purl.org/linked-data/sdmx/2009/concept#",
    "sdmx-measure": "http://purl.org/linked-data/sdmx/2009/measure#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "id": "urn:ngsi-ld:Dataset:dsd1",
  "language": {
    "type": "Property",
    "value": [
      "en",
      "fr"
    ]
  },
  "rdfs:label": {
    "type": "Property",
    "value": {
      "en": "Population by sex, age and local administrative unit",
      "fr": "Population par sexe, âge et unité administrative locale"
    }
  },
  "stat:attribute": {
    "type": "Property",
    "value": [
      "sdmx-attribute:unitMeasure",
      "isc:att-nuts3"
    ]
  },
  "stat:dimension": {
    "type": "Property",
    "value": [
      "isc:dim-age",
      "isc:dim-sex",
      "isc:dim-lau"
    ]
  },
  "stat:unitMeasure": {
    "type": "Property",
    "value": [
      "sdmx-measure:obsValue"
    ]
  },
  "title": {
    "type": "Property",
    "value": "dsd1"
  },
  "type": "Dataset"
}
"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
