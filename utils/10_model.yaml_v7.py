import pyaml
from github import Github


def open_jsonref(fileUrl):
	# function to retrieve either a json file from url or from disk
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
	# function to report a variable to be easily search in a long output
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def parse_payload(schemaPayload, level):
	# function which extracts the elements for the yaml output
    output = {}
    # parsing the first level of the object
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
					# parsing property individually
                    echo("parsing at level " + str(level) + " item= ", item)

                    if item == "description":
                        print("Detected property description=" + prop)
                        separatedDescription = str(schemaPayload["properties"][prop]["description"]).split(". ")
                        # this can be made simpler. to be changed
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
	# function to push a variable to a file in github
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
    result[dataModel]["type"] = "object"
    result[dataModel]["description"] = entityDescription
    result[dataModel]["required"] = required

    echo("result", result)

    path = dataModel + "/" + baseModelFileName
    message = "updated " + baseModelFileName
    github_push_from_variable(pyaml.dumps(result, width=4096), repoName, path, message, globalUser, token)

