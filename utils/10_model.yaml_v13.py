import pyaml
from github import Github
import requests
import datetime
import time


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


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def updated_raw_version_github(original_file_content, repository, path, timeout = 1000):
    uploaded = datetime.datetime.now() 
    remotepath = "https://raw.githubusercontent.com/smart-data-models/" + repository + "/master/" + path
    frequency = 5  # seconds
    counter = 0
    difference = True
    try:
        while difference:
            # text = requests.get(remotepath).content.decode('utf-8')[:-1]
            text = requests.get(remotepath).text[:-1]

            counter += frequency
            if counter > timeout:
                return False
            text = requests.get(remotepath).text

            print("retrieved test: " + text)
            print(ord(text[-1]))
            if str(text) == str(original_file_content):
                difference = False
                available = datetime.datetime.now()
                print("uploaded  at : " + str(uploaded))
                print("available at : " + str(available))
                return True
            else:
                print("______________________________________________")
                print(original_file_content)
                print("uploaded  at : " + str(uploaded))
                print("**********************************************")
                print(text)
                print("not matched at :" + str(datetime.datetime.now()))
                time.sleep(frequency)
    except (FileNotFoundError, IOError):
        print("file not available at : ")
        print("not matched at :" + str(datetime.datetime.now()))
        return False


def parse_description(schemaPayload):
    output = {}
    purgedDescription = str(schemaPayload["description"]).replace(chr(34), "")
    separatedDescription = purgedDescription. split(". ")
    copiedDescription = list.copy(separatedDescription)
    
    for descriptionPiece in separatedDescription:
        if descriptionPiece in propertyTypes:
            output["type"] = descriptionPiece
            copiedDescription.remove(descriptionPiece)
        elif descriptionPiece.find("Model:") > -1:
            copiedDescription.remove(descriptionPiece)
            output["model"] = descriptionPiece.replace("'", "").replace(
                    "Model:", "")

        if descriptionPiece.find("Units:") > -1:
            copiedDescription.remove(descriptionPiece)
            output["units"] = descriptionPiece.replace("'", "").replace(
                    "Units:", "")
    description = ". ".join(copiedDescription)

    return output, description


def parse_payload(schemaPayload, level):
    output = {}
    if level == 1:
        if "allOf" in schemaPayload:
            for index in range(len(schemaPayload["allOf"])):
                echo("passing to next level this payload=", str(schemaPayload["allOf"][index]))
                if "definitions" in schemaPayload["allOf"][index]:
                    partialOutput = parse_payload(schemaPayload["allOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["allOf"][index]:
                    partialOutput = parse_payload(schemaPayload["allOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput = parse_payload(schemaPayload["allOf"][index], level + 1)
                    output = dict(output, **partialOutput)
        if "anyOf" in schemaPayload:
            for index in range(len(schemaPayload["anyOf"])):
                echo("original output", output)
                if "definitions" in schemaPayload["anyOf"][index]:
                    partialOutput = parse_payload(schemaPayload["anyOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["anyOf"][index]:
                    partialOutput = parse_payload(schemaPayload["anyOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput = parse_payload(schemaPayload["anyOf"][index], level + 1)
                    output = dict(output, **partialOutput)
        if "oneOf" in schemaPayload:
            for index in range(len(schemaPayload["oneOf"])):
                echo("original output", output)
                if "definitions" in schemaPayload["oneOf"][index]:
                    partialOutput = parse_payload(schemaPayload["oneOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["oneOf"][index]:
                    partialOutput = parse_payload(schemaPayload["oneOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput = parse_payload(schemaPayload["oneOf"][index], level + 1)
                    output = dict(output, **partialOutput)

        if "properties" in schemaPayload:
            output = parse_payload(schemaPayload["properties"], level + 1)
                
    elif level < 8:
        if isinstance(schemaPayload, dict):
            for subschema in schemaPayload:
                if subschema in ["allOf", "anyOf", "oneOf"]:
                    output[subschema] = []
                    for index in range(len(schemaPayload[subschema])):
                        if "properties" in schemaPayload[subschema][index]:
                            partialOutput = parse_payload(schemaPayload[subschema][index], level + 1)
                            output[subschema].append(partialOutput["properties"])
                        else:
                            partialOutput = parse_payload(schemaPayload[subschema][index], level + 1)
                            output[subschema].append(partialOutput)
                
                elif subschema == "properties":
                    echo("properties level", level)
                    output[subschema] = {}
                    for prop in schemaPayload["properties"]:
                        echo(" dealing at level " + str(level) + " with prop=", prop)

                        echo("parsing this payload at " + str(level) + " from prop =" + prop, schemaPayload["properties"][prop])
                        try:
                            output[subschema][prop]
                        except:
                            output[subschema][prop] = {}
                        for item in list(schemaPayload["properties"][prop]):
                            echo("parsing at level " + str(level) + " item= ", item)

                            if item in ["allOf", "anyOf", "oneOf"]:
                                output[subschema][prop][item] = []
                                for index in range(len(schemaPayload[subschema][prop][item])):
                                    output[subschema][prop][item].append(parse_payload(schemaPayload[subschema][prop][item][index], level + 1))
                            elif item == "description":
                                print("Detectada la descripcion de la propiedad=" + prop)
                                x_ngsi, description = parse_description(schemaPayload[subschema][prop])
                                output[subschema][prop][item] = description
                                if x_ngsi:
                                    output[subschema][prop]["x-ngsi"] = x_ngsi
                            
                            elif item == "items":
                                output[subschema][prop][item] = parse_payload(schemaPayload[subschema][prop][item], level + 1)
                            elif item == "properties":
                                output[subschema][prop][item] = parse_payload(schemaPayload[subschema][prop][item], level + 1)
                            elif item == "type":
                                if schemaPayload[subschema][prop][item] == "integer":
                                    output[subschema][prop][item] = "number"
                                else:
                                    output[subschema][prop][item] = schemaPayload[subschema][prop][item]
                            else:
                                output[subschema][prop][item] = schemaPayload[subschema][prop][item]

                elif isinstance(schemaPayload[subschema], dict):        
                    output[subschema] = parse_payload(schemaPayload[subschema], level + 1)
                else:
                    if subschema == "description":
                        x_ngsi, description = parse_description(schemaPayload)
                        output[subschema] = description
                        if x_ngsi:
                            output["x-ngsi"] = x_ngsi
                    else:
                        output[subschema] = schemaPayload[subschema]
        
        elif isinstance(schemaPayload, list):
            for index in range(len(schemaPayload)):
                partialOutput = parse_payload(schemaPayload[index], level + 1)
                output = dict(output, **partialOutput)
    else:
        return None

    return output



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



baseModelFileName = "model.yaml"
#credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
credentialsFile = "/home/fiware/credentials.json"
credentials = open_jsonref(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
g = Github(token)

propertyTypes = ["Property", "Relationship", "GeoProperty"]


configFile = "datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)
print(dataModelsToPublish)
print(type(dataModelsToPublish))

echo("subject", dataModelsToPublish["subject"])
echo("dataModels", dataModelsToPublish["dataModels"])
echo("filter or no ", dataModelsToPublish["filterDataModels"])

repoName = dataModelsToPublish["subject"]
dataModels = dataModelsToPublish["dataModels"]
if isinstance(dataModels, str):
    dataModels = [dataModels] 
enableDataModelFilter = dataModelsToPublish["filterDataModels"]

for dataModel in dataModels:
    # have to be removed if the data model is fixed
    # if dataModel in ["WoodworkingMachine"]: continue
    echo("repoName", repoName)
    result = {}
    result[dataModel] = {}
    echo("dataModel=", dataModel)
    schemaUrl = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/schema.json"
    echo("urlschema", schemaUrl)
    schemaExpanded = open_jsonref(schemaUrl)
    echo("schemaExpanded", schemaExpanded)
    result[dataModel]["properties"] = parse_payload(schemaExpanded, 1)
    try:  # the required clause is optional
        required = schemaExpanded["required"]
    except:
        required = []
    try:
        entityDescription = schemaExpanded["description"].replace(chr(34),"")
    except:
        entityDescription = "No description available"
    try:
        version = schemaExpanded["$schemaVersion"]
    except:
        version = ""
    try:
        tags = schemaExpanded["modelTags"]
    except:
        tags = ""
    try:
        modelSchema = schemaExpanded["$id"]
    except:
        modelSchema = ""
    try:
        licenseUrl = schemaExpanded["licenseUrl"]
    except:
        licenseUrl = "https://github.com/smart-data-models/" + repoName + "/blob/master/" + dataModel + "/LICENSE.md"
    try:
        disclaimer = schemaExpanded["disclaimer"]
    except:
        disclaimer = "Redistribution and use in source and binary forms, with or without modification, are permitted  provided that the license conditions are met. Copyleft (c) 2022 Contributors to Smart Data Models Program"
    try:
        derivedFrom = schemaExpanded["derivedFrom"]
    except:
        derivedFrom = ""



    result[dataModel]["type"] = "object"
    result[dataModel]["description"] = entityDescription
    result[dataModel]["required"] = required
    result[dataModel]["x-version"] = version
    result[dataModel]["x-model-tags"] = tags
    result[dataModel]["x-model-schema"] = modelSchema
    result[dataModel]["x-license-url"] = licenseUrl
    result[dataModel]["x-disclaimer"] = disclaimer
    result[dataModel]["x-derived-from"] = derivedFrom


    echo("result", result)

    path = dataModel + "/" + baseModelFileName
    message = "updated " + baseModelFileName + " - support subproperties"
    # keep the original references when there are $ref clauses
    schema = open_json(schemaUrl)
    if "allOf" in schema:
        for cursor in range(len(schema["allOf"])):
            if "properties" in schema["allOf"][cursor]:
                for element in schema["allOf"][cursor]["properties"]:
                    if element in result[dataModel]["properties"]:
                        if "description" in schema["allOf"][cursor]["properties"][element] and "description" in result[dataModel]["properties"][element]:
                            _, description = parse_description(schema["allOf"][cursor]["properties"][element])
                            result[dataModel]["properties"][element]["description"] = description
                            print("replaced descripton in " + element + " to " + schema["allOf"][cursor]["properties"][element]["description"])
    else:
        print("Nothing to expand")

    content_variable = pyaml.dumps(result, width=4096, force_embed=True).decode("utf-8")
    github_push_from_variable(content_variable, repoName, path, message, globalUser, token)
    available = False
    while not available:
        available = updated_raw_version_github(content_variable, repoName, path)




