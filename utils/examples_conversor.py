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
  "location": {
    "type": "geo:json",
    "value": {
      "type": "Point",
      "coordinates": [
        -35.589575,
        -78.339812
      ]
    }
  },
  "address": {
    "type": "StructuredValue",
    "value": {
      "streetAddress": "Jai Singh Marg, Hanuman Road Area, Connaught Place",
      "addressLocality": "New Delhi",
      "addressRegion": "Delhi",
      "addressCountry": "India",
      "postalCode": "110001",
      "postOfficeBoxNumber": ""
    }
  },
  "areaServed": {
    "type": "Text",
    "value": ""
  },
  "id": "urn:ngsi-ld:SolarEnergy:id:BHDU:88967916",
  "dateCreated": {
    "type": "DateTime",
    "value": "2022-01-10T01:49:09Z"
  },
  "dateModified": {
    "type": "DateTime",
    "value": "2022-01-10T01:50:52Z"
  },
  "source": {
    "type": "Text",
    "value": ""
  },
  "name": {
    "type": "Text",
    "value": "Solar Energy measured at resource 1"
  },
  "alternateName": {
    "type": "Text",
    "value": "Solar energy source 1"
  },
  "description": {
    "type": "Text",
    "value": "Solar energy source 1"
  },
  "dataProvider": {
    "type": "Text",
    "value": ""
  },
  "owner": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:SolarEnergy:items:DACI:25767721",
      "urn:ngsi-ld:SolarEnergy:items:YVQJ:55840840"
    ]
  },
  "seeAlso": {
    "type": "array",
    "value": [
      "urn:ngsi-ld:SolarEnergy:items:XREG:08856151"
    ]
  },
  "type": "SolarEnergy",
  "totalActivePower": {
    "type": "Number",
    "value": 873.9
  },
  "phaseCurrent": {
    "type": "StructuredValue",
    "value": {
      "L1": 111.5,
      "L2": 109.3,
      "L3": 111.0
    }
  },
  "reactivePower": {
    "type": "StructuredValue",
    "value": {
      "L1": 108.1,
      "L2": 107.0,
      "L3": 106.5
    }
  },
  "voltage": {
    "type": "Number",
    "value": 122.0
  },
  "powerFactor": {
    "type": "StructuredValue",
    "value": {
      "L1": 0.7,
      "L2": 0.7,
      "L3": 0.5
    }
  },
  "current": {
    "type": "StructuredValue",
    "value": {
      "L1": 1.2,
      "L2": 1.2,
      "L3": 1.3,
      "N": 0.7
    }
  },
  "totalReactivePower": {
    "type": "Number",
    "value": 110.8
  },
  "phaseVoltage": {
    "type": "StructuredValue",
    "value": {
      "L1": 120.5,
      "L2": 116.4,
      "L3": 119.8
    }
  },
  "activePower": {
    "type": "StructuredValue",
    "value": {
      "L1": 17.3,
      "L2": 19.5,
      "L3": 20.4
    }
  },
  "dataDescriptor": {
    "type": "Relationship",
    "value": "urn:ngsi-ld:SolarEnergy:dataDescriptor:TTTK:11491249"
  },
  "energyGenerated": {
    "type": "Number",
    "value": 766.1
  },
  "maxSolarPowerMeasure": {
    "type": "Number",
    "value": 989.8
  },
  "frequency": {
    "type": "Number",
    "value": 50
  },
  "totalEnergyGenerated": {
    "type": "Number",
    "value": 527.6
  },
  "observationDateTime": {
    "type": "DateTime",
    "value": "2022-01-20T20:02:52Z"
  },
  "@context": [
    "https://smart-data-models.github.io/dataModel.Energy/context.jsonld"
  ]
}

"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
