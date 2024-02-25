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
################################################################################

# This file create a subject's @context file located in context.jsonld at root of the subject
import json
from datetime import datetime
from github import Github

import sys
from validator_collection import checkers
from pymongo import MongoClient

client = MongoClient()
db = client.smartdatamodels
col = db.properties

output = ""  # the variable containing the output. Focus on being printed in a web page
wrongPayload = False
processed = False
existing = False

def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")

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


def github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token):
    from github import Github
    g = Github(token)
    repo = g.get_organization(globalUser).get_repo(repoName)
    try:
        file = repo.get_contents("/" + fileTargetPath)
        update = True
    except:
        update = False
    if update:
        repo.update_file(fileTargetPath, message, contentVariable, file.sha)
    else:
        repo.create_file(fileTargetPath, message, contentVariable, "master")


def fake_subject():
    import string
    import random

    characters = string.ascii_letters + string.digits
    length = random.randint(5, 10)
    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

def extract_data_type(jsonPayload, item2=None):
    from validator_collection import checkers
    # expected a dict with the value of the attribute
    output = {}

    if item2:
        coreContextDictUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/context/ontologies_files/ngsi-ld-core-context.jsonld"
        etsiContext = open_json(coreContextDictUrl)['1.7']

        commonContextUrl = "https://github.com/smart-data-models/data-models/raw/master/context/common-context.jsonld"
        commonContext = open_json(commonContextUrl)['@context']

        if item2 in etsiContext:
            output[item2] = etsiContext[item2]
        elif item2 in commonContext:
            output[item2] = commonContext[item2]
        else:
            output[item2] = "https://smartdatamodels.org/" + subject + "/" + str(item2)

        jsonPayload = jsonPayload[item2]
    
    if checkers.is_dict(jsonPayload):
        for subitem in jsonPayload:
            subprop = extract_data_type(jsonPayload, subitem)
            output = dict(output, **subprop)
    elif checkers.is_iterable(jsonPayload):
        # print(" is array ")
        # print(jsonPayload)
        subprop = extract_data_type(jsonPayload[0])
        output = dict(output, **subprop)
    
    return output


propertyTypes = ["Property", "Relationship", "GeoProperty"]
contextDict = {"@context": {}}

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
    schemaPayload = {}
    subject = fake_subject()
    
    for item2 in payload:
        suboutput = extract_data_type(payload, item2)
        schemaPayload = dict(schemaPayload, **suboutput)
    
    processed = True


if processed and not wrongPayload:
    # print("________________")
    contextDict['@context'] = schemaPayload
    print(json.dumps(contextDict))
    with open("fake_context.json", "w") as file:
        json.dump(contextDict, file)

else:
    print(json.dumps(output))


# github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token)
# print(orderedContextDict)
