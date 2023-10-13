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


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


# main function for parsing the structured
def parse_payload_prop_and_type(schemaPayload, level):
    output = {}
    if "allOf" in schemaPayload:
        echo("allOf level", level)
        for index in range(len(schemaPayload["allOf"])):
            echo("passing to next level this payload=", str(schemaPayload["allOf"][index]))
            partialOutput = parse_payload_prop_and_type(schemaPayload["allOf"][index], level + 1)
            output = dict(output, **partialOutput)
    if "anyOf" in schemaPayload:
        echo("anyOf level", level)
        for index in range(len(schemaPayload["anyOf"])):
            echo("original output", output)
            partialOutput = parse_payload_prop_and_type(schemaPayload["anyOf"][index], level + 1)
            echo("parsed anyOf", partialOutput)
            output = dict(output, **partialOutput)
            echo("current output", output)
    if "oneOf" in schemaPayload:
        echo("oneOf level", level)
        for index in range(len(schemaPayload["oneOf"])):
            echo("original output", output)
            partialOutput = parse_payload_prop_and_type(schemaPayload["oneOf"][index], level + 1)
            echo("parsed oneOf", partialOutput)
            output = dict(output, **partialOutput)
            echo("current output", output)
    if "properties" in schemaPayload:
        echo("properties level", level)
        for prop in schemaPayload["properties"]:
            echo(" dealing at level " + str(level) + " with prop=", prop)
            if "allOf" in prop:
                echo("original output", output)
                echo("parsed allOf", partialOutput)
                output[prop] = parse_payload_prop_and_type(schemaPayload["properties"]["allOf"], level + 1)
            elif "anyOf" in prop:
                echo("original output", output)
                echo("parsed anyOf", partialOutput)
                output[prop] = parse_payload_prop_and_type(schemaPayload["properties"]["anyOf"], level + 1)
            elif "oneOf" in prop:
                echo("original output", output)
                echo("parsed oneOf", partialOutput)
                output[prop] = parse_payload_prop_and_type(schemaPayload["properties"]["oneOf"], level + 1)
            else:
                echo("parsing this payload at " + str(level) + " from prop =" + prop, schemaPayload["properties"][prop])
                try:
                    output[prop]
                except:
                    output[prop] = {}
                for item in list(schemaPayload["properties"][prop]):
                    echo("parsing at level " + str(level) + " item= ", item)

                    if item == "description":
                        print("Detected description of the property=" + prop)
                        separatedDescription = str(schemaPayload["properties"][prop]["description"]).split(". ")
                        copiedDescription = list.copy(separatedDescription)
                        print(copiedDescription)
                        for descriptionPiece in separatedDescription:
                            if descriptionPiece in propertyTypes:
                                print(descriptionPiece)
                                try:
                                    output[prop]["x-ngsi"]["type"] = descriptionPiece
                                except:
                                    output[prop]["x-ngsi"] = {}
                                    output[prop]["x-ngsi"]["type"] = descriptionPiece
                                copiedDescription.remove(descriptionPiece)
                                print(schemaPayload["properties"][prop])
                            elif descriptionPiece.find("Model:") > -1:
                                print(descriptionPiece)
                                copiedDescription.remove(descriptionPiece)
                                print(copiedDescription)
                                try:
                                    output[prop]["x-ngsi"]["model"] = descriptionPiece.replace("'", "").replace(
                                        "Model:", "")
                                except:
                                    output[prop]["x-ngsi"] = {}
                                    output[prop]["x-ngsi"]["model"] = descriptionPiece.replace("'", "").replace(
                                        "Model:", "")

                            if descriptionPiece.find("Units:") > -1:
                                print(descriptionPiece)
                                copiedDescription.remove(descriptionPiece)
                                print(copiedDescription)
                                try:
                                    output[prop]["x-ngsi"]["units"] = descriptionPiece.replace("'", "").replace(
                                        "Units:", "")
                                except:
                                    output[prop]["x-ngsi"] = {}
                                    output[prop]["x-ngsi"]["units"] = descriptionPiece.replace("'", "").replace(
                                        "Units:", "")
                        print("---")
                        description = ". ".join(copiedDescription)
                        output[prop]["description"] = description  # the remaining part of the description is used

                    elif item == "type":
                        output[prop]["type"] = schemaPayload["properties"][prop]["type"]
                    else:
                        echo("parsing prop", prop)
                        echo("payload", schemaPayload["properties"][prop][item])
                        output[prop][item] = schemaPayload["properties"][prop][item]
    return output


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


def open_yaml(fileUrl):
    import ruamel.yaml as yaml
    import requests
    try:
        if fileUrl[0:4] == "http":
            # es URL
            pointer = requests.get(fileUrl)
            return yaml.safe_load(pointer.content.decode('utf-8'))
    except:
        return "exception"
    else:
        # es file
        try:
            with open(fileUrl, "r") as file:
                return yaml.load(file)
            # file = open(fileUrl, "r")
            # return yaml.safe_load(file.read())
        except:
            return "wrong file"


def exist_page(url):
    # check if a web page exists
    # returns [true , web content] if successes
    # otherwise returns [false, error] if it fails
    import requests
    output = []
    try:
        pointer = requests.get(url)
        if pointer.status_code == 200:
            return [True, pointer.text]
        else:
            return [False, pointer.status_code]
    except:
        return [False, "wrong domain"]

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

def list_all_properties(repoName, modelYamlDict):
    contextDict = {"@context": {}}
    for item in modelYamlDict["properties"]:
        itemDict = modelYamlDict["properties"][item]

        try:
            itemKeys = list(modelYamlDict["properties"][item].keys())

            if "properties" in itemKeys:
                partialoutput = list_all_properties(repoName, modelYamlDict["properties"][item])
                contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])

            if itemDict["x-ngsi"]["type"] == "Relationship":
                # termType = "__Relationship"
                termType = ""
            elif itemDict["x-ngsi"]["type"] == "GeoProperty":
                # termType = "__Geoproperty"
                termType = ""
            elif itemDict["x-ngsi"]["type"] == "Property":
                operators = ["anyOf", "allOf", "oneOf"]
                if any(operator in itemKeys for operator in operators):
                    if "anyOf" in modelYamlDict["properties"][item]:
                        # termType = "__anyOf"
                        termType = ""
                    elif "allOf" in modelYamlDict["properties"][item]:
                        # termType = "__allOf"
                        termType = ""
                    elif "oneOf" in modelYamlDict["properties"][item]:
                        # termType = "__oneOf"
                        termType = ""
                else:
                    termType = ""
        except:
            termType = ""
            print(item)
            
        contextDict["@context"][str(item)] = "https://smartdatamodels.org/" + repoName + "/" + str(item) + termType
        
    return contextDict

def list_all_properties_v2(repoName, modelYamlDict):
    contextDict = {"@context": {}}
    if isinstance(modelYamlDict, list):
        for item in modelYamlDict:
            partialoutput = list_all_properties_v2(repoName, item)
            contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
    else:
        for prop in modelYamlDict:
            # print("prop ", prop)

            if isinstance(modelYamlDict[prop], list) and len(modelYamlDict[prop]) > 1 and isinstance(modelYamlDict[prop][0], dict):
                for item in modelYamlDict[prop]:
                    partialoutput = list_all_properties_v2(repoName, item)
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
    
            if isinstance(modelYamlDict[prop], dict):
                if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                    continue
                # print("dict prop ", prop)
                propKeys = list(modelYamlDict[prop].keys())

                # if there's type, and there's no items, allOf, properties
                # if type is a 
                if isinstance(modelYamlDict, dict) and ("type" in propKeys or "description" in propKeys) and prop != "x-ngsi":
                    # print("++++ context prop ", prop)
                    contextDict["@context"][str(prop)] = "https://smartdatamodels.org/" + repoName + "/" + str(prop)
                
                if "properties" in propKeys:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["properties"])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                if "items" in propKeys and modelYamlDict[prop]["items"]:
                    if isinstance(modelYamlDict[prop]["items"], list):
                        for index in range(len(modelYamlDict[prop]["items"])):
                            partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["items"][index])
                            contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                    else:
                        partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["items"])
                        contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                if "anyOf" in propKeys:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["anyOf"])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                if "allOf" in propKeys:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["allOf"])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                if "oneOf" in propKeys:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop]["oneOf"])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])   

    return contextDict


propertyTypes = ["Property", "Relationship", "GeoProperty"]
contextDict = {"@context": {}}

# credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
credentialsFile = "/home/fiware/credentials.json"
credentials = open_json(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
g = Github(token)

configFile = "datamodels_to_publish.json"
dataModelsToPublish = open_json(configFile)

# we have to update this file to the last version
coreContextDictUrl = "etsi_core_context.json"
coreContextDict = open_json(coreContextDictUrl)


dataModelsListUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
dataModelsList = open_json(dataModelsListUrl)["officialList"]
print(dataModelsList)

repoNames = [repo["repoName"] for repo in dataModelsList]

if dataModelsToPublish["subject"] in repoNames:
    repoName = dataModelsToPublish["subject"]
    index = repoNames.index(repoName)
    echo("index", index)
    dataModels = dataModelsList[index]["dataModels"]
    for dataModel in dataModels:
        echo("data Model", dataModel)
        urlModelYaml = "https://smart-data-models.github.io/" + repoName + "/" + dataModel + "/model.yaml"
        modelYamlDict = open_yaml(urlModelYaml)
# debug
        echo("repoNamsucoe", repoName)
        echo("dataModels", dataModels)
        echo("dataModel", dataModel)
        echo("urlModelYaml", urlModelYaml)
        echo("modelYamlDict", modelYamlDict)
# / debug  

        echo("modelYamlDict[dataModel][properties]", modelYamlDict[dataModel]["properties"])
        # important part 
        # we have to expand this from just one level to all levels
        ##########################################################
        tmpcontextDict = list_all_properties_v2(repoName, modelYamlDict[dataModel])
        contextDict["@context"] = dict(contextDict["@context"], **tmpcontextDict["@context"])
        echo("contextDict", contextDict)
        orderedContextDict = {"@context": {}}
        contextDict["@context"][dataModel] = "https://smartdatamodels.org/" + repoName + "/" + dataModel


        # replacing the elements which are in the common-schema.json
        commonContextUrl = "https://github.com/smart-data-models/data-models/raw/master/context/common-context.jsonld"
        commonContextDict = open_json(commonContextUrl)
        for item in commonContextDict["@context"]:
            if item in contextDict["@context"]:
                contextDict["@context"][item] = commonContextDict["@context"][item]
        contextDict["@context"]["ngsi-ld"] = coreContextDict["@context"]["ngsi-ld"]

        # including the elements of a customized context 
        urlCustomContext = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/notes_context.jsonld"
        existCustomContext = exist_page(urlCustomContext)
        if existCustomContext[0]:
            try:
                print(existCustomContext[1])
                customContextDict = json.loads(existCustomContext[1])
                for element in customContextDict:
                    print(item)
                    if element in contextDict["@context"]:
                        contextDict["@context"][element] = customContextDict[element]
            except:
                nada = 0 # error reading custom context, skipping

        # including the elements of the core NGSI-LD context
        for item in contextDict["@context"]:
            orderedContextDict["@context"][item] = contextDict["@context"][item]
            if item in coreContextDict["@context"]:
                orderedContextDict["@context"][item] = coreContextDict["@context"][item]

echo("orderedContextDict", orderedContextDict)
contentVariable = json.dumps(orderedContextDict, indent=4, sort_keys=True)
fileTargetPath = "context.jsonld"
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
message = "created/updated context - support subproperties at " + current_time

github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token)
# print(orderedContextDict)
