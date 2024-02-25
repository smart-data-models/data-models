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
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *"
    """
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")

def open_json(fileUrl):
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *"
    """
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
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *"
    """
    # import yaml
    from ruamel.yaml import YAML
    yaml_object = YAML(typ='safe', pure=True)
    import requests
    try:
        if fileUrl[0:4] == "http":
            # es URL
            pointer = requests.get(fileUrl)
            return yaml_object.load(pointer.content.decode('utf-8'))
    except:
        return "exception"
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return yaml_object.load(file.read())
        except:
            return "wrong file"

def exist_page(url):
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *", is_url_exist()
    """
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

@DeprecationWarning
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
    """
    Find all properties including the subproperties and create context

    Examples:
    >>> modelYamlDict = {"prop1": {"prop11", "prop12"}, .., "propn"}
    >>> list_all_properties_v2("datamodel.Weather", modelYamlDict)
    {
        "@context": {
            "prop1": "xxx/prop1",
            "prop11": "xxx/prop11",
            "prop12":` "xxx/prop12",
            ...
            "propn": "xxx/propn"
        }
    }
    """
    contextDict = {"@context": {}}

    # if the modelYamlDict is a list, then parse it individually
    if isinstance(modelYamlDict, list):
        for item in modelYamlDict:
            partialoutput = list_all_properties_v2(repoName, item)
            contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
    
    else:

        for prop in modelYamlDict:
            
            # Example: [{...}, {...}, ...]
            if isinstance(modelYamlDict[prop], list) and len(modelYamlDict[prop]) > 1 and isinstance(modelYamlDict[prop][0], dict):
                for item in modelYamlDict[prop]:
                    partialoutput = list_all_properties_v2(repoName, item)
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])

            # Example: {"description": xxx, "properties": xxx, "type": xxx, ...}
            if isinstance(modelYamlDict[prop], dict):

                # if prop equals to any value of "properties", "allOf", "oneOf", "anyOf", "items"
                # means the value of prop has deeper structure, like dictionary or list
                # so need to parse it one level deeper
                if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                    partialoutput = list_all_properties_v2(repoName, modelYamlDict[prop])
                    contextDict["@context"] = dict(contextDict["@context"], **partialoutput["@context"])
                    continue
                
                # Process the substructures 
                # Get the keys inside
                # Examples: {"description": xxx, "properties": xxx, "type": xxx, ...}
                # --> ["description", "properties", "type", ...]
                propKeys = list(modelYamlDict[prop].keys())

                # substructure is a dictionry and contains either type or description and name is not `x-ngsi`
                # so it is a candidate property
                if isinstance(modelYamlDict, dict) and ("type" in propKeys or "description" in propKeys) and prop != "x-ngsi":
                    
                    contextDict["@context"][str(prop)] = "https://smartdatamodels.org/" + repoName + "/" + str(prop)
                
                # TODO the following code could be simplied
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
        echo("repoName", repoName)
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
