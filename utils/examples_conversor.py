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

    if "id" in output:
        output["id"] = output["id"]["value"]
    if "type" in output:
        output["type"] = output["type"]["value"]
    if "@context" in output:
        output["@context"] = output["@context"]["value"]
    print(output)
    return output


keyvaluesPayload = {
  "id": "urn:ngsi-ld:dataModel:id:UZHW:27495447",
  "type": "Person",
  "dateCreated": "1993-05-07T06:43:37Z",
  "dateModified": "1978-12-27T04:25:34Z",
  "source": "Medical parent method become easy gas. South table fill finally rate morning. Evening trip whom serve year.",
  "name": "Capital seven level force add expert. Institution agree boy since agree allow.",
  "alternateName": "Treatment our process third offer data enjoy. Economy office government degree newspaper past life professional.",
  "description": "Peace economy student ball form. Avoid visit protect name. Our role challenge economy claim.",
  "dataProvider": "Suddenly nearly thank down. Visit safe soldier vote.",
  "owner": [
    "urn:ngsi-ld:dataModel:items:WQPT:65442393",
    "urn:ngsi-ld:dataModel:items:ALHV:33053523"
  ],
  "seeAlso": [
    "urn:ngsi-ld:dataModel:items:LHMU:67329694",
    "urn:ngsi-ld:dataModel:items:MMZQ:64123812"
  ],
  "location": {
    "type": "Point",
    "coordinates": [
      40.2403775,
      170.070362
    ]
  },
  "address": {
    "streetAddress": "Rock decide budget executive. Number who provide still despite Democrat money. Not gun box Democrat.",
    "addressLocality": "President feel film report point mother strategy. Public issue close too must safe officer. Focus enough well.",
    "addressRegion": "Hair hour avoid. World enjoy produce knowledge air population.",
    "addressCountry": "Hotel network investment sit money moment manager. He put husband play method simple.",
    "postalCode": "Word born success lose. Most become half relationship.",
    "postOfficeBoxNumber": "Pay shake night late situation admit. Peace relationship measure phone everything color. Itself us establish."
  },
  "areaServed": "Soldier company performance career prepare nearly. Woman how edge mouth.",
  "additionalName": "Possible outside soldier cultural professor experience wind. Area gun popular spring skin.",
  "familyName": "Future friend step card current. Than allow despite you their. White machine wrong state adult financial price.",
  "givenName": "Plant charge somebody feeling. Too man newspaper simply amount.",
  "telephone": "Team right area this stage any.",
  "email": "",
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}


normalizedPayload = """
{
  "id": "urn:ngsi-ld:AirQualityForecast:France-AirQualityForecast-12345_2022-07-01T18:00:00_2022-07-01T00:00:00",
  "type": "AirQualityForecast",
  "address": {
    "type": "Property",
    "value": {
      "addressCountry": "France",
      "postalCode": "06200",
      "addressLocality": "Nice",
      "type": "PostalAddress"
    }
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        7.2032497427380235,
        43.68056738083439
      ]
    }
  },
  "dataProvider": {
    "type": "Property",
    "value": "IMREDD_UCA_Nice"
  },
  "dateIssued": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T10:40:01.00Z"
    }
  },
  "dateRetrieved": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T12:57:24.00Z"
    }
  },
  "validFrom": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T17:00:00.00Z"
    }
  },
  "validTo": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2022-07-01T18:00:00.00Z"
    }
  },
  "validity": {
    "type": "Property",
    "value": "2022-07-01T17:00:00+01:00/2022-07-01T18:00:00+01:00"
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 3
  },
  "airQualityLevel": {
    "type": "Property",
    "value": "moderate"
  },
  "co2": {
    "type": "Property",
    "value": 45,
    "unitCode": "GQ"
  },
  "no2": {
    "type": "Property",
    "value": 69,
    "unitCode": "GQ"
  },
  "o3": {
    "type": "Property",
    "value": 100,
    "unitCode": "GQ"
  },
  "nox": {
    "type": "Property",
    "value": 139,
    "unitCode": "GQ"
  },
  "so2": {
    "type": "Property",
    "value": 11,
    "unitCode": "GQ"
  },
  "pm10": {
    "type": "Property",
    "value": 19,
    "unitCode": "GQ"
  },
  "pm25": {
    "type": "Property",
    "value": 21,
    "unitCode": "GQ"
  },
  "temperature": {
    "type": "Property",
    "value": 12.2
  },
  "relativeHumidity": {
    "type": "Property",
    "value": 0.54
  },
  "windSpeed": {
    "type": "Property",
    "value": 0.64
  },
  "precipitation": {
    "type": "Property",
    "value": 0
  },
  "typeOfLocation": {
    "type": "Property",
    "value": "outdoor"
  },
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://raw.githubusercontent.com/smart-data-models/dataModel.Environment/master/context.jsonld"
  ]
}
"""

# normalized2keyvalues(normalizedPayload)
keyvalues2normalized(keyvaluesPayload)
