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
# contact alberto.abella@fiware.org

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


def extract_data_type(jsonPayload):
    from validator_collection import checkers
    # expected a dict with the value of the attribute
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
            output["properties"][subitem] = extract_data_type(jsonPayload[subitem])
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
    return output


def gatherDefinitions(term):
    client = MongoClient()
    db = client.smartdatamodels
    col = db.properties
    query = {"property": term}
    attributesReturned = {"description": 1, "repoName": 1, "dataModel": 1}
    result = col.find(query, attributesReturned)
    definitions = []
    for element in result:
        removeId = element.pop("_id")
        if element not in dataModels:
            definitions.append(element)
    return definitions


unquotedPayload = sys.argv[1]  # 
rawPayload = securityParsing(unquotedPayload.replace(chr(39), chr(34)))
try:
    payload = json.loads(rawPayload)
except:
    wrongPayload = True
    payload = ""
    output = {"error" : "Not valid json. Payload", "payload": rawPayload}

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
    for item2 in payload:
        schemaItem = {}
        schemaItem = extract_data_type(payload[item2])
        # print("schemaItem=" + str(schemaItem))
        schemaPayload[item2] = schemaItem

        schemaPayload[item2]["description"] = "Property. "
        if item2 not in ["id", "type", "name", "address", "location", "dateCreated", "dateModified", "source", "alternateName", "description", "dataProvider", "owner", "seeAlso"]:
            # Looking for the same attribute in other data models
            description = gatherDefinitions(item2)
            # print("found description " + str(description))
            if len(description) > 0:
                if isinstance(description, dict):
                    description = [description]
                for subDesc in description:
                    schemaPayload[item2]["description"] += "Attribute present in data model " + subDesc["dataModel"] + " of subject " + subDesc["repoName"] + " with the description " + subDesc["description"] + ". "
        elif item2 == "id":
            schemaPayload[item2]["description"] = "Property. Unique identifier of the entity"
        elif item2 == "type":
            schemaPayload[item2]["description"] = "Property. NGSI Entity type. It has to be " + payload["type"]
            schemaPayload[item2]["enum"] = [payload["type"]]
        elif item2 == "name":
            schemaPayload[item2]["description"] = "Property. The name of this item. "
        elif item2 == "address":
            schemaPayload[item2]["description"] = "Property. The mailing address. Model:'https://schema.org/address'"
        elif item2 == "location":
            schemaPayload[item2]["description"] = "Geoproperty. Geojson reference to the item. It can be Point, LineString, Polygon, MultiPoint, MultiLineString or MultiPolygoProperty."
        elif item2 == "dateCreated":
            schemaPayload[item2]["description"] = "Property. Entity creation timestamp. This will usually be allocated by the storage platform"
        elif item2 == "dateModified":
            schemaPayload[item2]["description"] = "Property. Timestamp of the last modification of the entity. This will usually be allocated by the storage platform."
        elif item2 == "source":
            schemaPayload[item2]["description"] = "Property. A sequence of characters giving the original source of the entity data as a URL. Recommended to be the fully qualified domain name of the source provider, or the URL to the source object."
        elif item2 == "alternateName":
            schemaPayload[item2]["description"] = "Property. An alternative name for this item"
        elif item2 == "description":
            schemaPayload[item2]["description"] = "Property. A description of this item"
        elif item2 == "dataProvider":
            schemaPayload[item2]["description"] = "Property. A sequence of characters identifying the provider of the harmonised data entity"
        elif item2 == "owner":
            schemaPayload[item2]["description"] = "Property. A List containing a JSON encoded sequence of characters referencing the unique Ids of the owner(s)"
        elif item2 == "seeAlso":
            schemaPayload[item2]["description"] = "Property. List of uri pointing to additional resources about the item"

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
