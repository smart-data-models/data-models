import pyaml
from github import Github


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


def parse_payload(schemaPayload, level):
    output = {}
    if "allOf" in schemaPayload:
        echo("allOf level", level)
        for index in range(len(schemaPayload["allOf"])):
            echo("passing to next level this payload=", str(schemaPayload["allOf"][index]))
            partialOutput = parse_payload(schemaPayload["allOf"][index], level + 1)
            output = dict(output, **partialOutput)
    if "anyOf" in schemaPayload:
        echo("anyOf level", level)
        for index in range(len(schemaPayload["anyOf"])):
            echo("original output", output)
            partialOutput = parse_payload(schemaPayload["anyOf"][index], level + 1)
            echo("parsed anyOf", partialOutput)
            output = dict(output, **partialOutput)
            echo("current output", output)
    if "properties" in schemaPayload:
        echo("properties level", level)
        for prop in schemaPayload["properties"]:
            echo(" dealing at level " + str(level) + " with prop=", prop)
            if "allOf" in prop:
                echo("original output", output)
                echo("parsed allOf", partialOutput)
                output[prop] = parse_payload(schemaPayload["properties"]["allOf"], level + 1)
            elif "anyOf" in prop:
                echo("original output", output)
                echo("parsed anyOf", partialOutput)
                output[prop] = parse_payload(schemaPayload["properties"]["anyOf"], level + 1)
            else:
                echo("parsing this payload at " + str(level) + " from prop =" + prop, schemaPayload["properties"][prop])
                try:
                    output[prop]
                except:
                    output[prop] = {}
                for item in list(schemaPayload["properties"][prop]):
                    echo("parsing at level " + str(level) + " item= ", item)

                    if item == "description":
                        print("Detectada la descripcion de la propiedad=" + prop)
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

propertyTypes = ["Property", "Relationship", "Geoproperty"]


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
        entityDescription = schemaExpanded["description"]
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
        disclaimer = "Redistribution and use in source and binary forms, with or without modification, are permitted  provided that the license conditions are met. Copyleft (c) 2021 Contributors to Smart Data Models Program"
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
    message = "updated " + baseModelFileName
    github_push_from_variable(pyaml.dumps(result, width=4096), repoName, path, message, globalUser, token)

