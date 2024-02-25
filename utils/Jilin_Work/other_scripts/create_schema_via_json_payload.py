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
#  limitations under the License.
#  Author: alberto.abella@fiware.org
################################################################################

# This program will create a json schema based on one submitted key-values payload submitted through a web form

import sys
import json
from validator_collection import checkers
from pymongo import MongoClient

client = MongoClient()
db = client.smartdatamodels
col = db.properties

output = ""  # the variable containing the output. Focus on being printed in a web page
wrongPayload = False
processed = False
existing = False

def securityParsing(jsonPayload):
    # this functions will remove those element that are considered 'dangerous'
    return (jsonPayload)

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

def open_jsonref(fileUrl):
    import jsonref
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return jsonref.loads(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return jsonref.loads(file.read())


def validate_iso8601(str_val):
    import re
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(str_val) is not None:
            return True
    except:
        pass
    return False

def remove_trailing_period_and_spaces(sentence):
    import re
    pattern = r'\.\s+$'  
    return re.sub(pattern, '', sentence)


def extract_data_type(jsonPayload, item2=None):
    from validator_collection import checkers
    # expected a dict with the value of the attribute

    item2Description = "Property. "
    if item2:
        coreContextDictUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/context/ontologies_files/ngsi-ld-core-context.jsonld"
        etsiContext = open_json(coreContextDictUrl)['1.7']

        commonContextUrl = "https://github.com/smart-data-models/data-models/raw/master/context/common-context.jsonld"
        commonContext = open_json(commonContextUrl)['@context']

        if item2 in etsiContext or item2 in commonContext:
            description = gatherDefinitions(item2, True)
            if len(description) > 0:
                description = description[0]
                item2Description = description["typeNGSI"] + ". "
                if "model" in description:
                    item2Description += description["model"] + ". "
                if "units" in description:
                    item2Description += description["units"] + ". "
                item2Description += description["description"]
        else:
            description = gatherDefinitions(item2, False)
            if len(description) > 0:
                if isinstance(description, dict):
                    description = [description]
                for subDesc in description:
                    if not "description" in subDesc:
                        subDesc["description"] = ""
                    item2Description += "Attribute present in data model " + subDesc["dataModel"] + " of subject " + subDesc["repoName"] + " with the description " + remove_trailing_period_and_spaces(subDesc["description"]) + ". "

        jsonPayload = jsonPayload[item2]
    
    output = False
    if checkers.is_date(jsonPayload):
        # print(" is date ")
        output = {"type": "string", "format": "date-time"}
    elif checkers.is_numeric(jsonPayload):
        # print(" is number ")
        output = {"type": "number"}
    elif validate_iso8601(jsonPayload):
        # print(" is date time ")
        output = {"type": "string", "format": "date-time"}
    elif checkers.is_dict(jsonPayload):
        # print(" is object ")
        output = {"type": "object", "properties": {}}
        for subitem in jsonPayload:
            output["properties"][subitem] = extract_data_type(jsonPayload, subitem)
    elif checkers.is_iterable(jsonPayload):
        # print(" is array ")
        # print(jsonPayload)
        output = {"type": "array", "items": extract_data_type(jsonPayload[0])}
    elif checkers.is_string(jsonPayload):
        # print(" is string ")
        output = {"type": "string"}
    else:
        pass
        # print(" I do not know what type is it" + jsonPayload)

    output["description"] = item2Description
    
    return output


def gatherDefinitions(term, isSystemAttr=False):
    client = MongoClient()
    db = client.smartdatamodels
    col = db.properties
    query = {"property": term}
    if not isSystemAttr:
        attributesReturned = {"description": 1, "repoName": 1, "dataModel": 1}
        result = col.find(query, attributesReturned)
    else:
        result = col.find(query).limit(1)
    definitions = []
    for element in result:
        removeId = element.pop("_id")
        if element not in dataModels:
            definitions.append(element)
    return definitions


# unquotedPayload = sys.argv[1]  # 
# rawPayload = securityParsing(unquotedPayload.replace(chr(39), chr(34)))
# try:
#     payload = json.loads(rawPayload)
# except:
#     wrongPayload = True
#     payload = ""
#     output = {"error" : "Not valid json. Payload", "payload": rawPayload}

payload = open_json("./example_payload.json")

if not wrongPayload:
    if not checkers.is_json(payload):
        output = {"error": "Not valid json. checker", "payload": payload}
        wrongPayload = True
    else:
        keys = payload.keys()
        if "type" not in keys:
            # check that it is a valid entity (has a type)
            output = {"error": "Payload has not an attribute 'type'", "payload": payload}
            wrongPayload = True
        else:
            # check that it is not a repeated entity
            query = {"dataModel": payload["type"]}
            attributesReturned = {"dataModel": 1, "repoName": 1}
            result = col.find(query, attributesReturned)
            dataModels = []
            for element in result:
                removeId = element.pop("_id")
                if element not in dataModels:
                    dataModels.append(element)
            if len(dataModels) > 0:
                dataModelsStrings = ["https://github.com/smart-data-models/" + d["repoName"] + "/blob/master/" + d[
                    "dataModel"] + "/doc/spec.md" for d in dataModels]
                dataModelsIssues = ["https://github.com/smart-data-models/" + d["repoName"] + "/issues/new" for d in dataModels]
                dataModelsList = " <br>".join(dataModelsStrings)
                issuesList = " <br>".join(dataModelsIssues)
                output = {"found": "Entity type already available in Smart Data Models Program. Check these data Models", "dataModels": dataModelsStrings, "interact": " <br> if necessary (i.e. extend the model) raise an issue in these links " + issuesList}
                existing = True

if not wrongPayload and not existing:
    schemaHeader = {
        "$schema": "http://json-schema.org/schema#",
        "$schemaVersion": "0.0.1",
        "modelTags": "",
        "derivedFrom":"",
        "license": "",
        "$id": "https://smart-data-models.github.io/XXXsubjectXXX/XXXdataModelXXX/schema.json",
        "title": "",
        "description": "",
        "type": "object",
        "allOf": [
            {
                "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/GSMA-Commons"
            },
            {
                "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/Location-Commons"
            }
        ]
    }
    schema = schemaHeader
    schemaPayload = {}
    exceptions = ["id", "type", "name", "address", "location", "dateCreated", "dateModified", "source", "alternateName", "description", "dataProvider", "owner", "seeAlso"]

    # in extract_data_type --> definition about the subproperties
    # properties from common-schema.json
    #       if properties from common-schema.json, then take the description from it
    #           if properties from GSMA-Commons, and Location-Commons, then don't show it
    #           else show the description
    #       else looking for the same attribute in other data models

    for item2 in payload:
        schemaItem = {}

        if item2 == "type":
            schemaPayload[item2] = {}
            schemaPayload[item2]["description"] = "Property. NGSI Entity type. It has to be " + payload["type"]
            schemaPayload[item2]["enum"] = [payload["type"]]
        elif not item2 in exceptions:
            schemaItem = extract_data_type(payload, item2)
            # print("schemaItem=" + str(schemaItem))
            schemaPayload[item2] = schemaItem

    schema["allOf"].append({"properties": schemaPayload})
    schema["required"] = ["id", "type"]
    output = schema
    processed = True
    # print(schema)


if processed and not wrongPayload:
    # print("________________")
    print(json.dumps(output))
    with open("schema.json", "w") as file:
        json.dump(schema, file)

        # function to check if one element is in the database
        # gather payload from form
else:
    print(json.dumps(output))
