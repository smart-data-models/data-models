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

# This file run converts the API output of an open data soft portal into a draft schema for Smart Data Models
# version 0.4
# 22-8-22
help = """
          Parameters:
              base url of the ODS portal
              dataset_id of the dataset

          Returns:
             A draft json schema compliant with Smart Data Models Program,
             some limitations: it does not translate descriptions (required in English)
             some data types
             it prints the schema and also returns (if possible a file named schema.json)

          test it with this 
            SDM_OpenDataSoft_schema_converter.py https://data.ameli.fr/ effectifs

          """

import sys
import json


def open_json(fileUrl):
    import json
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            return json.loads(pointer.content.decode('utf-8'))
        except:
            return None

    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return json.loads(file.read())
        except:
            return None


def convertQuotes(inputText):
    output = inputText.replace(chr(34), "'")
    return output


def convertType(odsType):
    # peding to identify all types in ODS
    if odsType == "text":
        output = "string"
    elif odsType == "integer":
        output = "number"
    elif odsType == "double":
        output = "number"
    else:
        output = "new type " + odsType
    return output


input = sys.argv
if input[1] == "--help" or input[1] == "-h":
    print(help)
    sys.exit(0)
elif len(input) < 3:
    sys.exit(1)
else:
    # base url of the ODS portal
    urlPortal = sys.argv[1]
    # dataset_id of the dataset
    dataset_id = sys.argv[2]

try:
    # url of the dataset api structure
    url = urlPortal + "/api/v2/catalog/datasets/" + dataset_id
    # print(url)
    structureDict = open_json(url)
    # print(structureDict)
    attributes = structureDict["dataset"]["fields"]
    metas = structureDict["dataset"]["metas"]
except:
    sys.exit(1)

# print(attributes)

urlTemplateSDM = "https://raw.githubusercontent.com/smart-data-models/data-models/master/templates/dataModel/schema.json"
schemaTemplate = open_json(urlTemplateSDM)
schema = schemaTemplate.copy()
schemaTemplate["title"] = metas["default"]["title"]
schemaTemplate["description"] = convertQuotes(metas["default"]["description"])
schemaTemplate["modelTags"] = metas["default"]["keyword"]
schemaTemplate["license"] = metas["default"]["license_url"]
schemaTemplate["allOf"][2]["properties"]["type"]["description"] = dataset_id
schemaTemplate["allOf"][2]["properties"]["type"]["enum"] = dataset_id

for item in attributes:
    field = {}
    entityName = item["name"]
    # print(entityName)
    field[entityName] = {}
    # print(field)
    # print(item)
    field[entityName]["type"] = convertType(item["type"])
    field[entityName]["description"] = "Property. " + str(item["description"])
    schemaTemplate["allOf"][2]["properties"][entityName] = field[entityName]

print(schemaTemplate)
try:
    with open("schema.json", "w") as fileOutput:
        fileOutput.write(json.dumps(schemaTemplate, sort_keys=False, indent=4))
except:
    print("possibly lack of permissions to write the output")