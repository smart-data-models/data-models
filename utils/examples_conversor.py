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
    with open("output.json", "w") as outputfile:
        rawoutput = json.dumps(output, indent=4)
        outputfile.write(rawoutput)
    return output


keyvaluesPayload = {
  "resourceType": "Immunization",
  "id": "urn:ngsi-ld:example",
  "text": {
    "status": "generated",
    "div": "\u003cdiv xmlns\u003d\"http://www.w3.org/1999/xhtml\"\u003e\u003cp\u003e\u003cb\u003eGenerated Narrative\u003c/b\u003e\u003c/p\u003e\u003cdiv style\u003d\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"\u003e\u003cp style\u003d\"margin-bottom: 0px\"\u003eResource \u0026quot;example\u0026quot; \u003c/p\u003e\u003c/div\u003e\u003cp\u003e\u003cb\u003eidentifier\u003c/b\u003e: id: urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234\u003c/p\u003e\u003cp\u003e\u003cb\u003estatus\u003c/b\u003e: completed\u003c/p\u003e\u003cp\u003e\u003cb\u003evaccineCode\u003c/b\u003e: Fluvax (Influenza) \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (unknown#FLUVAX)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003epatient\u003c/b\u003e: \u003ca href\u003d\"patient-example.html\"\u003ePatient/example\u003c/a\u003e \u0026quot;Peter CHALMERS\u0026quot;\u003c/p\u003e\u003cp\u003e\u003cb\u003eencounter\u003c/b\u003e: \u003ca href\u003d\"encounter-example.html\"\u003eEncounter/example\u003c/a\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003eoccurrence\u003c/b\u003e: 2013-01-10\u003c/p\u003e\u003cp\u003e\u003cb\u003eprimarySource\u003c/b\u003e: true\u003c/p\u003e\u003cp\u003e\u003cb\u003elocation\u003c/b\u003e: \u003ca href\u003d\"location-1.html\"\u003eLocation/1\u003c/a\u003e \u0026quot;South Wing, second floor\u0026quot;\u003c/p\u003e\u003cp\u003e\u003cb\u003emanufacturer\u003c/b\u003e: \u003ca href\u003d\"organization-hl7.html\"\u003eOrganization/hl7\u003c/a\u003e \u0026quot;Health Level Seven International\u0026quot;\u003c/p\u003e\u003cp\u003e\u003cb\u003elotNumber\u003c/b\u003e: AAJN11K\u003c/p\u003e\u003cp\u003e\u003cb\u003eexpirationDate\u003c/b\u003e: 2015-02-15\u003c/p\u003e\u003cp\u003e\u003cb\u003esite\u003c/b\u003e: left arm \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v3-ActSite.html\"\u003eActSite\u003c/a\u003e#LA)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003eroute\u003c/b\u003e: Injection, intramuscular \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v3-RouteOfAdministration.html\"\u003eRouteOfAdministration\u003c/a\u003e#IM)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003edoseQuantity\u003c/b\u003e: 5 mg\u003cspan style\u003d\"background: LightGoldenRodYellow\"\u003e (Details: UCUM code mg \u003d \u0027mg\u0027)\u003c/span\u003e\u003c/p\u003e\u003cblockquote\u003e\u003cp\u003e\u003cb\u003eperformer\u003c/b\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003efunction\u003c/b\u003e: Ordering Provider \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v2-0443.html\"\u003eproviderRole\u003c/a\u003e#OP)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003eactor\u003c/b\u003e: \u003ca href\u003d\"practitioner-example.html\"\u003ePractitioner/example\u003c/a\u003e \u0026quot;Adam CAREFUL\u0026quot;\u003c/p\u003e\u003c/blockquote\u003e\u003cblockquote\u003e\u003cp\u003e\u003cb\u003eperformer\u003c/b\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003efunction\u003c/b\u003e: Administering Provider \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v2-0443.html\"\u003eproviderRole\u003c/a\u003e#AP)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003eactor\u003c/b\u003e: \u003ca href\u003d\"practitioner-example.html\"\u003ePractitioner/example\u003c/a\u003e \u0026quot;Adam CAREFUL\u0026quot;\u003c/p\u003e\u003c/blockquote\u003e\u003cp\u003e\u003cb\u003enote\u003c/b\u003e: Notes on adminstration of vaccine\u003c/p\u003e\u003cp\u003e\u003cb\u003ereasonCode\u003c/b\u003e: Procedure to meet occupational requirement \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"https://browser.ihtsdotools.org/\"\u003eSNOMED CT\u003c/a\u003e#429060002)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003eisSubpotent\u003c/b\u003e: true\u003c/p\u003e\u003ch3\u003eEducations\u003c/h3\u003e\u003ctable class\u003d\"grid\"\u003e\u003ctr\u003e\u003ctd\u003e-\u003c/td\u003e\u003ctd\u003e\u003cb\u003eDocumentType\u003c/b\u003e\u003c/td\u003e\u003ctd\u003e\u003cb\u003ePublicationDate\u003c/b\u003e\u003c/td\u003e\u003ctd\u003e\u003cb\u003ePresentationDate\u003c/b\u003e\u003c/td\u003e\u003c/tr\u003e\u003ctr\u003e\u003ctd\u003e*\u003c/td\u003e\u003ctd\u003e253088698300010311120702\u003c/td\u003e\u003ctd\u003e2012-07-02\u003c/td\u003e\u003ctd\u003e2013-01-10\u003c/td\u003e\u003c/tr\u003e\u003c/table\u003e\u003cp\u003e\u003cb\u003eprogramEligibility\u003c/b\u003e: Not Eligible \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"codesystem-immunization-program-eligibility.html\"\u003eImmunization Event Program Eligibility\u003c/a\u003e#ineligible)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003efundingSource\u003c/b\u003e: Private \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"codesystem-immunization-funding-source.html\"\u003eImmunization Event Funding Source\u003c/a\u003e#private)\u003c/span\u003e\u003c/p\u003e\u003c/div\u003e"
  },
  "identifier": [
    {
      "system": "urn:ietf:rfc:3986",
      "value": "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234"
    }
  ],
  "status": "completed",
  "vaccineCode": {
    "coding": [
      {
        "system": "urn:oid:1.2.36.1.2001.1005.17",
        "code": "FLUVAX"
      }
    ],
    "text": "Fluvax (Influenza)"
  },
  "patient": {
    "reference": "Patient/example"
  },
  "encounter": {
    "reference": "Encounter/example"
  },
  "occurrenceDateTime": "2013-01-10",
  "primarySource": True,
  "location": {
    "reference": "Location/1"
  },
  "manufacturer": {
    "reference": "Organization/hl7"
  },
  "lotNumber": "AAJN11K",
  "expirationDate": "2015-02-15",
  "site": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite",
        "code": "LA",
        "display": "left arm"
      }
    ]
  },
  "route": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration",
        "code": "IM",
        "display": "Injection, intramuscular"
      }
    ]
  },
  "doseQuantity": {
    "value": 5,
    "system": "http://unitsofmeasure.org",
    "code": "mg"
  },
  "performer": [
    {
      "function": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
            "code": "OP"
          }
        ]
      },
      "actor": {
        "reference": "Practitioner/example"
      }
    },
    {
      "function": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
            "code": "AP"
          }
        ]
      },
      "actor": {
        "reference": "Practitioner/example"
      }
    }
  ],
  "note": [
    {
      "text": "Notes on adminstration of vaccine"
    }
  ],
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "429060002"
        }
      ]
    }
  ],
  "isSubpotent": True,
  "education": [
    {
      "documentType": "253088698300010311120702",
      "publicationDate": "2012-07-02",
      "presentationDate": "2013-01-10"
    }
  ],
  "programEligibility": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/immunization-program-eligibility",
          "code": "ineligible"
        }
      ]
    }
  ],
  "fundingSource": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/immunization-funding-source",
        "code": "private"
      }
    ]
  },
  "meta": {
    "tag": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
        "code": "HTEST",
        "display": "test health data"
      }
    ]
  }
}

normalizedPayload = """
{
  "id": "urn:ngsi-ld:FishContainment:1",
  "type": "FishContainment",
  "category": {
    "type": "Property",
    "value": "Tank"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [
        0,
        0
      ]
    }
  },
  "refSump": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Sump:1"
  },
  "refFarm": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Farm:1"
  },
  "depth": {
    "type": "Property",
    "value": 10,
    "unitCode": "MTR"
  },
  "videoStream": {
    "type": "Property",
    "value": "stream URL",
    "observedBy": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Device:camera:01"
    },
    "depth": {
      "type": "Property",
      "value": 10,
      "unitCode": "MTR"
    }
  },
  "temperature": [
    {
      "type": "Property",
      "value": 15.2,
      "unitCode": "CEL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:temperature:Device:01"
    },
    {
      "type": "Property",
      "value": 16.1,
      "unitCode": "CEL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 5,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:Device:02"
      },
      "datasetId": "urn:ngsi-ld:Dataset:temperature:Device:02"
    }
  ],
  "dissolvedOxygen": [
    {
      "type": "Property",
      "value": 80,
      "unitCode": "P1",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relat{
  "resourceType": "Medication",
  "id": "med0301",
  "type" : "Medication",
  "text": {
    "status": "generated",
    "div": "\u003cdiv xmlns\u003d\"http://www.w3.org/1999/xhtml\"\u003e\u003cp\u003e\u003cb\u003eGenerated Narrative\u003c/b\u003e\u003c/p\u003e\u003cdiv style\u003d\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"\u003e\u003cp style\u003d\"margin-bottom: 0px\"\u003eResource \u0026quot;med0301\u0026quot; \u003c/p\u003e\u003c/div\u003e\u003cp\u003e\u003cb\u003ecode\u003c/b\u003e: Vancomycin Hydrochloride (VANCOMYCIN HYDROCHLORIDE) \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v3-ndc.html\"\u003eNational drug codes\u003c/a\u003e#0409-6531-02)\u003c/span\u003e\u003c/p\u003e\u003cp\u003e\u003cb\u003estatus\u003c/b\u003e: active\u003c/p\u003e\u003cp\u003e\u003cb\u003emanufacturer\u003c/b\u003e: \u003ca name\u003d\"org4\"\u003e \u003c/a\u003e\u003c/p\u003e\u003cblockquote\u003e\u003cdiv style\u003d\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"\u003e\u003cp style\u003d\"margin-bottom: 0px\"\u003eResource \u0026quot;org4\u0026quot; \u003c/p\u003e\u003c/div\u003e\u003cp\u003e\u003cb\u003ename\u003c/b\u003e: Pfizer Laboratories Div Pfizer Inc\u003c/p\u003e\u003c/blockquote\u003e\u003cp\u003e\u003cb\u003eform\u003c/b\u003e: Injection Solution (qualifier value) \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"https://browser.ihtsdotools.org/\"\u003eSNOMED CT\u003c/a\u003e#385219001)\u003c/span\u003e\u003c/p\u003e\u003ch3\u003eIngredients\u003c/h3\u003e\u003ctable class\u003d\"grid\"\u003e\u003ctr\u003e\u003ctd\u003e-\u003c/td\u003e\u003ctd\u003e\u003cb\u003eItem[x]\u003c/b\u003e\u003c/td\u003e\u003ctd\u003e\u003cb\u003eIsActive\u003c/b\u003e\u003c/td\u003e\u003ctd\u003e\u003cb\u003eStrength\u003c/b\u003e\u003c/td\u003e\u003c/tr\u003e\u003ctr\u003e\u003ctd\u003e*\u003c/td\u003e\u003ctd\u003eVancomycin Hydrochloride \u003cspan style\u003d\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"\u003e (\u003ca href\u003d\"http://terminology.hl7.org/3.1.0/CodeSystem-v3-rxNorm.html\"\u003eRxNorm\u003c/a\u003e#66955)\u003c/span\u003e\u003c/td\u003e\u003ctd\u003etrue\u003c/td\u003e\u003ctd\u003e500 mg\u003cspan style\u003d\"background: LightGoldenRodYellow\"\u003e (Details: UCUM code mg \u003d \u0027mg\u0027)\u003c/span\u003e/10 mL\u003cspan style\u003d\"background: LightGoldenRodYellow\"\u003e (Details: UCUM code mL \u003d \u0027mL\u0027)\u003c/span\u003e\u003c/td\u003e\u003c/tr\u003e\u003c/table\u003e\u003ch3\u003eBatches\u003c/h3\u003e\u003ctable class\u003d\"grid\"\u003e\u003ctr\u003e\u003ctd\u003e-\u003c/td\u003e\u003ctd\u003e\u003cb\u003eLotNumber\u003c/b\u003e\u003c/td\u003e\u003ctd\u003e\u003cb\u003eExpirationDate\u003c/b\u003e\u003c/td\u003e\u003c/tr\u003e\u003ctr\u003e\u003ctd\u003e*\u003c/td\u003e\u003ctd\u003e9494788\u003c/td\u003e\u003ctd\u003e2017-05-22\u003c/td\u003e\u003c/tr\u003e\u003c/table\u003e\u003c/div\u003e"
  },
  "contained": [
    {
      "resourceType": "Organization",
      "id": "org4",
      "name": "Pfizer Laboratories Div Pfizer Inc"
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://hl7.org/fhir/sid/ndc",
        "code": "0409-6531-02",
        "display": "Vancomycin Hydrochloride (VANCOMYCIN HYDROCHLORIDE)"
      }
    ]
  },
  "status": "active",
  "manufacturer": {
    "reference": "#org4"
  },
  "form": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "385219001",
        "display": "Injection Solution (qualifier value)"
      }
    ]
  },
  "ingredient": [
    {
      "itemCodeableConcept": {
        "coding": [
          {
            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
            "code": "66955",
            "display": "Vancomycin Hydrochloride"
          }
        ]
      },
      "isActive": true,
      "strength": {
        "numerator": {
          "value": 500,
          "system": "http://unitsofmeasure.org",
          "code": "mg"
        },
        "denominator": {
          "value": 10,
          "system": "http://unitsofmeasure.org",
          "code": "mL"
        }
      }
    }
  ],
  "batch": {
    "lotNumber": "9494788",
    "expirationDate": "2017-05-22"
  },
  "meta": {
    "tag": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
        "code": "HTEST",
        "display": "test health data"
      }
    ]
  }
}ionship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:dissolvedOxygen:P1:Device:01"
    },
    {
      "type": "Property",
      "value": 5.4,
      "unitCode": "M1",
      "observedAt": "2020-08-31T11:31:29.000Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:dissolvedOxygen:M1:Device:01"
    }
  ],
  "pH": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "Q30",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:pH:Device:01"
    }
  ],
  "redoxPotential": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "2Z",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:redoxPotential:Device:01"
    }
  ],
  "turbidity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "NTU",
      "observedAt": "2020-06-26T21:32:52z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:turbidity:NTU:Device:01"
    },
    {
      "type": "Property",
      "value": 0,
      "unitCode": "FNU",
      "observedAt": "2020-08-31T11:31:29.000Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:turbidity:FNU:Device:01"
    }
  ],
  "conductivity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "NTU",
      "observedAt": "2020-06-26T21:32:52+02:00",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:aquabox:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:conductivity:NTU:aquabox01"
    }
  ],
  "salinity": [
    {
      "type": "Property",
      "value": 7,
      "unitCode": "GL",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:salinity:GL:Device:01"
    }
  ],
  "totalDissolvedSolids": [
    {
      "type": "Property",
      "value": 35404,
      "unitCode": "G42",
      "observedAt": "2020-06-26T21:32:52Z",
      "depth": {
        "type": "Property",
        "value": 10,
        "unitCode": "MTR"
      },
      "observedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Device:01"
      },
      "datasetId": "urn:ngsi-ld:Dataset:totalDissolvedSolids:G42:Device:01"
    }
  ],
  "marineCurrents": {
    "type": "Property",
    "value": "NA",
    "observedAt": "2021-05-04T08:30:00Z"
  },
  "feedingOperation": {
    "type": "Property",
    "refFeeder": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:Feeder:AUTO"
    },
    "observation": {
      "type": "Property",
      "value": "NA"
    },
    "threats": {
      "type": "Property",
      "value": "NA"
    },
    "value": 10,
    "observedAt": "2021-05-04T08:30:00Z",
    "unitCode": "KGM",
    "endedAt": {
      "type": "Property",
      "value": {
        "type": "DateTime",
        "@value": "2021-05-04T18:00:00Z"
      }
    },
    "startedAt": {
      "type": "Property",
      "value": {
        "type": "DateTime",
        "@value": "2021-05-04T08:30:00Z"
      }
    }
  },
  "fishDensity": [
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean0To1",
      "value": -26.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean1To2",
      "value": -24.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean2To3",
      "value": -15.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean3To4",
      "value": -18.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean4To5",
      "value": -27.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean5To6",
      "value": -26.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean6To7",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean7To8",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean8To9",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    },
    {
      "type": "Property",
      "datasetId": "urn:ngsi-ld:Dataset:mean9o10",
      "value": -25.0,
      "observedAt": "2021-10-19T14:22:19Z"
    }
  ],
  "fishSpeed": {
    "type": "Property",
    "value": 25.0,
    "unitCode": "",
    "observedAt": "2021-10-19T14:22:19Z"
  },
  "fishDirection": {
    "type": "Property",
    "value": "SW",
    "observedAt": "2021-10-19T14:22:19Z"
  },
  "@context": [
    "https://raw.githubusercontent.com/smart-data-models/data-models/master/context.jsonld"
  ]
}
"""

# normalized2keyvalues(normalizedPayload)
schema = keyvalues2normalized(keyvaluesPayload)
with open("keyvalues.json", "w") as file:
    json.dump(schema, file)
