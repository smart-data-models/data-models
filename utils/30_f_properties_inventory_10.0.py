#################################################################################
#  Licensed to the FIWARE Foundation (FF) under one                             #
#  or more contributor license agreements. The FF licenses this file            #
#  to you under the Apache License, Version 2.0 (the "License")                 #
#  you may not use this file except in compliance with the License.             #
#  You may obtain a copy of the License at                                      #
#                                                                               #
#      http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                               #
#  Unless required by applicable law or agreed to in writing, software          #
#  distributed under the License is distributed on an "AS IS" BASIS,            #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     #
#  See the License for the specific language governing permissions and          #
#  limitations under the License.                                               #
#################################################################################
import sys
import json


def open_yaml(fileUrl):
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
        return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return yaml_object.load(file.read())
        except:
            return None


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


def properties_inventory(repoName, dataModel):
    #################################################################################
    # This file updates the properties compiled in the smart data models repository #
    # call for a repo and a data model                                              #
    #################################################################################
    from pymongo import MongoClient

    #################################################################################
    #   Static parameters of smart data models initiative mongodb database          #
    #################################################################################
    urlDataModelsList = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
    dataModelsList = open_jsonref(urlDataModelsList)["officialList"]
    dbName = "smartdatamodels"
    collectionPropertiesName = "properties"
    credentialsFile = "/home/fiware/credentials.json"
    # credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"

    #                                                                               #
    #################################################################################

    #################################################################################
    #   parsing input parameters                                                     #
    #################################################################################
    repoNames = [repoItem["repoName"] for repoItem in dataModelsList]
    if repoName not in repoNames:
        return [False, "Not found repoName"]
    dataModels = [dataModelItem for repoItem in dataModelsList for dataModelItem in repoItem["dataModels"]]
    if dataModel not in dataModels:
        return [False, "Not found dataModel"]
    #                                                                               #
    #################################################################################

    client = MongoClient()
    db = client[dbName]
    collProperties = db[collectionPropertiesName]
    collProperties.delete_many({"repoName": repoName, "dataModel": dataModel})

    schemaYaml = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/model.yaml"

    schema = open_yaml(schemaYaml)[dataModel]
    print(schema)

    coreContextDictUrl = "etsi_core_context.json"
    etsiContext = open_json(coreContextDictUrl)['@context']

    subjectContextUrl = f"https://raw.githubusercontent.com/smart-data-models/{repoName}/master/context.jsonld"
    orderedContextDict = open_json(subjectContextUrl)

    if "x-version" in schema:
        schemaVersion = schema["x-version"]
    else:
        schemaVersion = ""
    if "x-model-tags" in schema:
        modelTags = schema["x-model-tags"]
    else:
        modelTags = ""
    if "x-license-url" in schema:
        license = schema["x-license-url"]
    else:
        license = ""

    def insert_property_item(modelYamlDict, level, parentId="", parent=""):
        """
        same structure as the function list_all_properties_v2 in 25_create_subject_context_V7.py
        expect the way of dealing with the found property and insert operation

        Find all properties including the subproperties and insert property into mongodb
        """

        # if the modelYamlDict is a list, then parse it individually
        if isinstance(modelYamlDict, list):
            for item in modelYamlDict:
                insert_property_item(item, level + 1, "")

        else:

            for prop in modelYamlDict:

                # Example: [{...}, {...}, ...]
                if isinstance(modelYamlDict[prop], list) and len(modelYamlDict[prop]) > 1 and isinstance(
                        modelYamlDict[prop][0], dict):
                    for item in modelYamlDict[prop]:
                        insert_property_item(item, level + 1, "")

                # Example: {"description": xxx, "properties": xxx, "type": xxx, ...}
                if isinstance(modelYamlDict[prop], dict):

                    # if prop equals to any value of "properties", "allOf", "oneOf", "anyOf", "items"
                    # means the value of prop has deeper structure, like dictionary or list
                    # so need to parse it one level deeper
                    if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                        insert_property_item(modelYamlDict[prop], level + 1, "")
                        continue

                    # Process the substructures
                    # Get the keys inside
                    # Examples: {"description": xxx, "properties": xxx, "type": xxx, ...}
                    # --> ["description", "properties", "type", ...]
                    propKeys = list(modelYamlDict[prop].keys())

                    # substructure is a dictionry and contains either type or description and name is not `x-ngsi`
                    # so it is a candidate property
                    if isinstance(modelYamlDict, dict) and (
                            "type" in propKeys or "description" in propKeys) and prop != "x-ngsi":

                        if parentId:
                            # if parentId exists, property is a subproperty
                            # create id using parentId
                            # Example: parentId: "xxx/prop1/#" -> id: "xxx/prop1/prop11/#"
                            id = parentId.replace('#', f'/{prop}#')

                        else:
                            # if parentId doesn't exist, then create its own id
                            id = f"https://smartdatamodels.org/{repoName}/{dataModel}/{prop}#{schemaVersion}"

                        # create the property item, including
                        # "prop": {
                        #     "id": "",
                        #     "description": "",
                        #     "property": "",
                        #     "datamodel": "",
                        #     "subject": "",
                        #     ...
                        # }
                        propDict, _ = create_property_item({prop: modelYamlDict[prop]}, parentId, parent)

                        print("inserting this element in the properties' collection")
                        print(propDict)
                        collProperties.insert_one(propDict)

                    if "properties" in propKeys:
                        insert_property_item(modelYamlDict[prop]["properties"], level + 1, id, prop)
                    if "items" in propKeys and modelYamlDict[prop]["items"]:
                        if isinstance(modelYamlDict[prop]["items"], list):
                            for index in range(len(modelYamlDict[prop]["items"])):
                                insert_property_item(modelYamlDict[prop]["items"][index], level + 1)
                        else:
                            insert_property_item(modelYamlDict[prop]["items"], level + 1)
                    if "anyOf" in propKeys:
                        insert_property_item(modelYamlDict[prop]["anyOf"], level + 1)
                    if "allOf" in propKeys:
                        insert_property_item(modelYamlDict[prop]["allOf"], level + 1)
                    if "oneOf" in propKeys:
                        insert_property_item(modelYamlDict[prop]["oneOf"], level + 1)

    def create_property_item(schemaPayload, parentId="", parent=""):
        """
        Create property item for mongodb

        Parameters:
        - schemaPayload (dict): the schema payload of the property
        - parentId (str): the id of parental property
        - parent (str): the name of parental property
        """

        subproperties = []  # deal with subproperty case

        # parse the structure of the property individually
        for item in schemaPayload:

            parsedDescripton = False
            parsedXNGSI = False
            propDict = {}

            # create id, parentId, parentContext if there's parental property
            if parentId:
                propDict["id"] = parentId.replace('#', f'/{item}#')
                if parent in etsiContext:  # replace with the etsi pre-defined ones
                    if not isinstance(etsiContext[parent], str):
                        left, right = etsiContext[parent]['@id'].split(":")
                        propDict["parentContext"] = etsiContext[left] + right
                    elif ("http" in etsiContext[parent]) or ("@" in etsiContext[parent]):
                        propDict["parentContext"] = etsiContext[parent]
                    else:
                        left, right = etsiContext[parent].split(":")
                        propDict["parentContext"] = etsiContext[left] + right
                else:
                    propDict["parentContext"] = orderedContextDict["@context"][parent]
                propDict["parentId"] = parentId
            else:
                propDict["id"] = f"https://smartdatamodels.org/{repoName}/{dataModel}/{item}#{schemaVersion}"

            # create context
            if item in etsiContext:  # replace with the etsi pre-defined ones
                if not isinstance(etsiContext[item], str):
                    left, right = etsiContext[item]['@id'].split(":")
                    propDict["context"] = etsiContext[left] + right
                elif ("http" in etsiContext[item]) or ("@" in etsiContext[item]):
                    propDict["context"] = etsiContext[item]
                else:
                    left, right = etsiContext[item].split(":")
                    propDict["context"] = etsiContext[left] + right
            else:
                propDict["context"] = orderedContextDict["@context"][item]
            subproperties.append({item: propDict["context"]})

            propDict["property"] = item
            propDict["dataModel"] = dataModel
            propDict["repoName"] = repoName
            propDict["modelTags"] = modelTags
            propDict["license"] = license  # this is here but this is not sent to the mysql database
            propDict["schemaVersion"] = schemaVersion

            try:
                itemKeys = list(schemaPayload[item].keys())
                if "properties" in itemKeys:
                    _, subprops = create_property_item(schemaPayload[item]["properties"], parentId=propDict["id"],
                                                       parent=item)
                    propDict["subpropertiesContext"] = subprops
                if "type" in schemaPayload[item]:
                    propDict["type"] = schemaPayload[item]["type"]
                    if "format" in schemaPayload[item]:
                        propDict["format"] = schemaPayload[item]["format"]
                    if "description" in schemaPayload[item]:
                        print("prop: " + item)
                        propDict["description"] = schemaPayload[item]["description"]
                    if "x-ngsi" in schemaPayload[item]:
                        if "type" in schemaPayload[item]["x-ngsi"]:
                            propDict["typeNGSI"] = schemaPayload[item]["x-ngsi"]["type"]
                        if "model" in schemaPayload[item]["x-ngsi"]:
                            propDict["model"] = schemaPayload[item]["x-ngsi"]["model"]
                        if "units" in schemaPayload[item]["x-ngsi"]:
                            propDict["units"] = schemaPayload[item]["x-ngsi"]["units"]
                    if "enum" in schemaPayload[item]:
                        propDict["enum"] = schemaPayload[item]["enum"]
                    if "privacy" in schemaPayload[item]:
                        propDict["privacy"] = schemaPayload[item]["privacy"]

                elif any([x in schemaPayload[item] for x in ["anyOf", "oneOf", "allOf"]]):
                    # print("________________________________________________")
                    # print(schemaPayload[item])
                    # print("________________________________________________")

                    whichClause = list(schemaPayload[item].keys())[0]
                    # print("________________________________________________")
                    # print(whichClause)
                    # print("________________________________________________")
                    itemPayload = schemaPayload[item][whichClause][0]

                    if "type" in itemPayload:
                        propDict["type"] = itemPayload["type"]

                    if "format" in itemPayload:
                        propDict["format"] = itemPayload["format"]

                    if "description" in schemaPayload[item]:
                        print("prop: " + item)
                        propDict["description"] = schemaPayload[item]["description"]
                    if "x-ngsi" in schemaPayload[item]:
                        if "type" in schemaPayload[item]["x-ngsi"]:
                            propDict["typeNGSI"] = schemaPayload[item]["x-ngsi"]["type"]
                        if "model" in schemaPayload[item]["x-ngsi"]:
                            propDict["model"] = schemaPayload[item]["x-ngsi"]["model"]
                        if "units" in schemaPayload[item]["x-ngsi"]:
                            propDict["units"] = schemaPayload[item]["x-ngsi"]["units"]
                    if "enum" in itemPayload:
                        propDict["enum"] = itemPayload["enum"]
                    if "privacy" in itemPayload:
                        propDict["privacy"] = itemPayload["privacy"]
                    else:
                        print("prop: " + item)
            except:
                print(item)

        return propDict, subproperties

    schemaPayload = schema["properties"]
    insert_property_item(schemaPayload, 1)


def open_jsonref(fileUrl):
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *"
    """
    import jsonref
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True)
            return output
        except:
            return ""
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read())
        except:
            return ""


configFile = "datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)
repoName = dataModelsToPublish["subject"]
dataModels = dataModelsToPublish["dataModels"]
if isinstance(dataModels, str):
    dataModels = [dataModels]
print(dataModels)
for dataModel in dataModels:
    properties_inventory(repoName, dataModel)

