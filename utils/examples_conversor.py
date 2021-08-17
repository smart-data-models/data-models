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
  "id": "urn:ngsi-ld:AirQualityMonitoring:id:ARET:00795717",
  "type": "AirQualityMonitoring",
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2017-12-31T03:39:27Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2021-12-22T04:21:57Z"
    }
  },
  "source": {
    "type": "Property",
    "value": "Bangalore Smart city"
  },
  "name": {
    "type": "Property",
    "value": ""
  },
  "alternateName": {
    "type": "Property",
    "value": "EnvAQM sampling"
  },
  "description": {
    "type": "Property",
    "value": "Air quality monitoring"
  },
  "dataProvider": {
    "type": "Property",
    "value": ""
  },
  "owner": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:AirQualityMonitoring:items:WCBR:34036943",
      "urn:ngsi-ld:AirQualityMonitoring:items:PLLV:16542546"
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:AirQualityMonitoring:items:FCTF:59597941",
      "urn:ngsi-ld:AirQualityMonitoring:items:JAYJ:76906163"
    ]
  },
  "location": {
    "type": "Property",
    "value": {
      "type": "Point",
      "coordinates": [
        12.979,
        77.591
      ]
    }
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "Avenue Road",
      "addressLocality": "Bangalore",
      "addressRegion": "Karnataka",
      "addressCountry": "India",
      "postalCode": "110001",
      "postOfficeBoxNumber": ""
    }
  },
  "areaServed": {
    "type": "Property",
    "value": "Bangalore"
  },
  "deviceInfo": {
    "type": "Property",
    "value": {
      "deviceList": "12",
      "deviceBatteryStatus": "Connected",
      "deviceName": "Climo",
      "deviceID": "12345",
      "RFID": "AB463478",
      "measurand": "",
      "deviceSimNumber": "12345678",
      "deviceModel": {
        "brandName": "Climo",
        "manufacturerName": "Bosch",
        "modelName": "sensor",
        "modelURL": "www.boschclimo.com",
        "areaServed": "Agartala"
      },
      "refDevice": "urn:ngsi-ld:device:12"
    }
  },
  "observationDateTime": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2020-09-16T11:00:00+05:30"
    }
  },
  "deviceStatus": {
    "type": "Property",
    "value": "ACTIVE"
  },
  "atmosphericPressure": {
    "type": "Property",
    "value": 633.2
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 90
  },
  "airQualityLevel": {
    "type": "Property",
    "value": "SATISFACTORY"
  },
  "aqiMajorPollutant": {
    "type": "Property",
    "value": "No2"
  },
  "airTemperatureTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 23.1,
      "minOverTime": 12.7,
      "maxOverTime": 32.8,
      "instValue": 30.8
    }
  },
  "ambientNoiseTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 57.9,
      "minOverTime": 50.5,
      "maxOverTime": 59.2,
      "instValue": 57.6
    }
  },
  "arsenicTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 0.4,
      "minOverTime": 0.29,
      "maxOverTime": 0.44,
      "instValue": 0.35
    }
  },
  "atmosphericPressureTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 968.3,
      "minOverTime": 961.9,
      "maxOverTime": 982.7,
      "instValue": 982.9
    }
  },
  "bapTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 492.1,
      "minOverTime": 398.7,
      "maxOverTime": 573.7,
      "instValue": 439.1
    }
  },
  "benzeneTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 266.7,
      "minOverTime": 210.1,
      "maxOverTime": 576.9,
      "instValue": 321.7
    }
  },
  "coTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.51,
      "minOverTime": 3.4,
      "maxOverTime": 8.9,
      "instValue": 4.0
    }
  },
  "co2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 318.51,
      "minOverTime": 302.6,
      "maxOverTime": 390.2,
      "instValue": 320.4
    }
  },
  "nh3TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 865.1,
      "minOverTime": 834.7,
      "maxOverTime": 990.8,
      "instValue": 900.2
    }
  },
  "nickelTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 434.0,
      "minOverTime": 132.2,
      "maxOverTime": 559.6,
      "instValue": 527.2
    }
  },
  "noTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.65,
      "minOverTime": 2.7,
      "maxOverTime": 4.8,
      "instValue": 3.6
    }
  },
  "no2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 409.7,
      "minOverTime": 242.4,
      "maxOverTime": 611.5,
      "instValue": 511.0
    }
  },
  "o2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 18.1,
      "minOverTime": 18.0,
      "maxOverTime": 18.2,
      "instValue": 18.0
    }
  },
  "o3TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 218.8,
      "minOverTime": 167.7,
      "maxOverTime": 236.4,
      "instValue": 173.1
    }
  },
  "pm10TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 847.3,
      "minOverTime": 54.3,
      "maxOverTime": 568.1,
      "instValue": 439.1
    }
  },
  "pm25TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 28.3,
      "minOverTime": 10.1,
      "maxOverTime": 56.8,
      "instValue": 56.6
    }
  },
  "relativeHumidityTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 326.3,
      "minOverTime": 211.6,
      "maxOverTime": 599.3,
      "instValue": 401.2
    }
  },
  "so2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.65,
      "minOverTime": 2.9,
      "maxOverTime": 3.72,
      "instValue": 3.5
    }
  },
  "pbTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 473.0,
      "minOverTime": 287.5,
      "maxOverTime": 542.1,
      "instValue": 391.0
    }
  },
  "uvTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 6.0,
      "minOverTime": 5.7,
      "maxOverTime": 8.3,
      "instValue": 8.2
    }
  },
  "illuminance": {
    "type": "Property",
    "value": 3319.41
  },
  "solarRadiation": {
    "type": "Property",
    "value": 3.65
  },
  "precipitation": {
    "type": "Property",
    "value": 846.0
  },
  "versionInfo": {
    "type": "Property",
    "value": {
      "startDateTime": {
        "@type": "DateTime",
        "@value": "2020-09-16T11:00:00+05:30"
      },
      "endDateTime": {
        "@type": "DateTime",
        "@value": "2020-09-16T11:00:00+05:30"
      },
      "versionName": "Version 1",
      "comments": "Version 1"
    }
  },
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}



"""


normalizedPayload = """
{
  "id": "urn:ngsi-ld:AirQualityMonitoring:id:ARET:00795717",
  "type": "AirQualityMonitoring",
  "dateCreated": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2017-12-31T03:39:27Z"
    }
  },
  "dateModified": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2021-12-22T04:21:57Z"
    }
  },
  "source": {
    "type": "Property",
    "value": "Bangalore Smart city"
  },
  "name": {
    "type": "Property",
    "value": ""
  },
  "alternateName": {
    "type": "Property",
    "value": "EnvAQM sampling"
  },
  "description": {
    "type": "Property",
    "value": "Air quality monitoring"
  },
  "dataProvider": {
    "type": "Property",
    "value": ""
  },
  "owner": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:AirQualityMonitoring:items:WCBR:34036943",
      "urn:ngsi-ld:AirQualityMonitoring:items:PLLV:16542546"
    ]
  },
  "seeAlso": {
    "type": "Property",
    "value": [
      "urn:ngsi-ld:AirQualityMonitoring:items:FCTF:59597941",
      "urn:ngsi-ld:AirQualityMonitoring:items:JAYJ:76906163"
    ]
  },
  "location": {
    "type": "Property",
    "value": {
      "type": "Point",
      "coordinates": [
        12.979,
        77.591
      ]
    }
  },
  "address": {
    "type": "Property",
    "value": {
      "streetAddress": "Avenue Road",
      "addressLocality": "Bangalore",
      "addressRegion": "Karnataka",
      "addressCountry": "India",
      "postalCode": "110001",
      "postOfficeBoxNumber": ""
    }
  },
  "areaServed": {
    "type": "Property",
    "value": "Bangalore"
  },
  "deviceInfo": {
    "type": "Property",
    "value": {
      "deviceList": "12",
      "deviceBatteryStatus": "Connected",
      "deviceName": "Climo",
      "deviceID": "12345",
      "RFID": "AB463478",
      "measurand": "",
      "deviceSimNumber": "12345678",
      "deviceModel": {
        "brandName": "Climo",
        "manufacturerName": "Bosch",
        "modelName": "sensor",
        "modelURL": "www.boschclimo.com",
        "areaServed": "Agartala"
      },
      "refDevice": "urn:ngsi-ld:device:12"
    }
  },
  "observationDateTime": {
    "type": "Property",
    "value": {
      "@type": "DateTime",
      "@value": "2020-09-16T11:00:00+05:30"
    }
  },
  "deviceStatus": {
    "type": "Property",
    "value": "ACTIVE"
  },
  "atmosphericPressure": {
    "type": "Property",
    "value": 633.2
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 90
  },
  "airQualityLevel": {
    "type": "Property",
    "value": "SATISFACTORY"
  },
  "aqiMajorPollutant": {
    "type": "Property",
    "value": "No2"
  },
  "airTemperatureTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 23.1,
      "minOverTime": 12.7,
      "maxOverTime": 32.8,
      "instValue": 30.8
    }
  },
  "ambientNoiseTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 57.9,
      "minOverTime": 50.5,
      "maxOverTime": 59.2,
      "instValue": 57.6
    }
  },
  "arsenicTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 0.4,
      "minOverTime": 0.29,
      "maxOverTime": 0.44,
      "instValue": 0.35
    }
  },
  "atmosphericPressureTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 968.3,
      "minOverTime": 961.9,
      "maxOverTime": 982.7,
      "instValue": 982.9
    }
  },
  "bapTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 492.1,
      "minOverTime": 398.7,
      "maxOverTime": 573.7,
      "instValue": 439.1
    }
  },
  "benzeneTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 266.7,
      "minOverTime": 210.1,
      "maxOverTime": 576.9,
      "instValue": 321.7
    }
  },
  "coTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.51,
      "minOverTime": 3.4,
      "maxOverTime": 8.9,
      "instValue": 4.0
    }
  },
  "co2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 318.51,
      "minOverTime": 302.6,
      "maxOverTime": 390.2,
      "instValue": 320.4
    }
  },
  "nh3TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 865.1,
      "minOverTime": 834.7,
      "maxOverTime": 990.8,
      "instValue": 900.2
    }
  },
  "nickelTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 434.0,
      "minOverTime": 132.2,
      "maxOverTime": 559.6,
      "instValue": 527.2
    }
  },
  "noTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.65,
      "minOverTime": 2.7,
      "maxOverTime": 4.8,
      "instValue": 3.6
    }
  },
  "no2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 409.7,
      "minOverTime": 242.4,
      "maxOverTime": 611.5,
      "instValue": 511.0
    }
  },
  "o2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 18.1,
      "minOverTime": 18.0,
      "maxOverTime": 18.2,
      "instValue": 18.0
    }
  },
  "o3TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 218.8,
      "minOverTime": 167.7,
      "maxOverTime": 236.4,
      "instValue": 173.1
    }
  },
  "pm10TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 847.3,
      "minOverTime": 54.3,
      "maxOverTime": 568.1,
      "instValue": 439.1
    }
  },
  "pm25TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 28.3,
      "minOverTime": 10.1,
      "maxOverTime": 56.8,
      "instValue": 56.6
    }
  },
  "relativeHumidityTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 326.3,
      "minOverTime": 211.6,
      "maxOverTime": 599.3,
      "instValue": 401.2
    }
  },
  "so2TSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 3.65,
      "minOverTime": 2.9,
      "maxOverTime": 3.72,
      "instValue": 3.5
    }
  },
  "pbTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 473.0,
      "minOverTime": 287.5,
      "maxOverTime": 542.1,
      "instValue": 391.0
    }
  },
  "uvTSA": {
    "type": "Property",
    "value": {
      "avgOverTime": 6.0,
      "minOverTime": 5.7,
      "maxOverTime": 8.3,
      "instValue": 8.2
    }
  },
  "illuminance": {
    "type": "Property",
    "value": 3319.41
  },
  "solarRadiation": {
    "type": "Property",
    "value": 3.65
  },
  "precipitation": {
    "type": "Property",
    "value": 846.0
  },
  "versionInfo": {
    "type": "Property",
    "value": {
      "startDateTime": {
        "@type": "DateTime",
        "@value": "2020-09-16T11:00:00+05:30"
      },
      "endDateTime": {
        "@type": "DateTime",
        "@value": "2020-09-16T11:00:00+05:30"
      },
      "versionName": "Version 1",
      "comments": "Version 1"
    }
  },
  "@context": [
    "https://smartdatamodels.org/context.jsonld"
  ]
}

"""

normalized2keyvalues(normalizedPayload)
# keyvalues2normalized(keyvaluesPayload)
