# This program generates automatically the swagger.yaml for each data model
from github import Github
import yaml

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


def open_json(fileUrl):
    import json
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return json.loads(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return json.loads(file.read())


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


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def read_github_file(fileName, repoName):
    from github import Github

    credentialsFile = "/home/fiware/credentials.json"
    credentials = open_json(credentialsFile)
    token = credentials["token"]
    g = Github(token)
    globalUser = credentials["globalUser"]

    repository = g.get_organization(globalUser).get_repo(repoName)
    file_content = repository.get_contents(fileName)
    return file_content.decoded_content.decode()


def read_yaml(fileUrl):
    import yaml
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return yaml.safe_load(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return yaml.safe_load.loads(file.read())


def github_delete_file_push(originalPath, repoName, message, globalUser, token):
    from github import Github

    g = Github(token)
    repo = g.get_organization(globalUser).get_repo(repoName)
    try:
        destinyObject = repo.get_contents(originalPath)
        destinyFileExist = True
    except:
        destinyFileExist = False
    if destinyFileExist:
        commit = repo.delete_file(originalPath, message, destinyObject.sha)
        return [True, commit]
    else:
        return [False, "not found"]

#credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
credentialsFile = "/home/fiware/credentials.json"
credentials = open_json(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
g = Github(token)

configFile ="datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)


echo("subject", dataModelsToPublish["subject"])
echo("dataModels", dataModelsToPublish["dataModels"])
echo("filter or no ", dataModelsToPublish["filterDataModels"])
echo("languages ", dataModelsToPublish["languages"])


repoName = dataModelsToPublish["subject"]
dataModels = dataModelsToPublish["dataModels"]

# CONSTANTS
modelYaml = "model.yaml"
swaggerHeader = """---
# Copyleft (c) 2022 Contributors to Smart Data Models initiative
# """
swaggerBody = """paths: 
  /ngsi-ld/v1/entities: 
    get: 
      description: "Retrieve a set of entities which matches a specific query from an NGSI-LD system"
      parameters: 
        - 
          in: query
          name: type
          required: true
          schema: 
            enum: 
              - Building
            type: string
      responses: 
        ? "200"
        : 
          content: 
            application/ld+json: 
              examples: 
                keyvalues: 
                  summary: "Key-Values Pairs"
                  value: 
                    - 
                      $ref: "https://smart-data-models.github.io/dataModel.Building/Building/examples/example.json"
                normalized: 
                  summary: "Normalized NGSI-LD"
                  value: 
                    - 
                      $ref: "https://smart-data-models.github.io/dataModel.Building/Building/examples/example-normalized.jsonld"
          description: OK
      tags: 
        - ngsi-ld
tags: 
  - 
    description: "NGSI-LD Linked-data Format"
    name: ngsi-ld"""
tab = "  "
nl = chr(10)
rootModelUrl = "https://smart-data-models.github.io/"
outputFile = "test.yaml"
# CONSTANTS #


for dataModel in dataModels:  
    pathModelYaml = "/" + dataModel + "/" + modelYaml
    try:
        modelContent = read_github_file(pathModelYaml, repoName)
        print(type(modelContent))
        modelPresent = True
        print(modelContent)
        modelDict = yaml.safe_load(modelContent)
    except:
        modelPresent = False
    if modelPresent:
        swaggerContent = swaggerHeader + nl
        swaggerContent += nl
        swaggerContent += nl
        swaggerContent += "components:" + nl
        swaggerContent += 1 * tab + "schemas: " + nl
        swaggerContent += 2 * tab + dataModel + ": " + nl
        swaggerContent += 3 * tab + "$ref: " + chr(34) + rootModelUrl + repoName + "/" + dataModel + "/" + modelYaml + "#/" + dataModel + chr(34) + nl
        swaggerContent += "info:" + nl
        swaggerContent += 1 * tab + "description:  |" + nl
        if "description" in modelDict[dataModel]:
            swaggerContent += 2 * tab + modelDict[dataModel]["description"] + nl
        swaggerContent += 1 * tab + "title: " + dataModel + nl
        swaggerContent += 1 * tab + "version: " + chr(34) + modelDict[dataModel]["x-version"] + chr(34) + nl
        swaggerContent += "openapi: " + chr(34) + "3.0.0" + chr(34) + nl
        swaggerContent += nl
        customBody = swaggerBody.replace("- Building", "- " + dataModel).replace("/dataModel.Building/Building/", "/" + repoName + "/" + dataModel + "/")

        for line in customBody.splitlines():
            print(line)
            swaggerContent += line + nl
        print(swaggerContent)
        #with open(outputFile, "w") as output:
        #    output.write(swaggerContent)

        ##############################################################
        # remove the old swagger.yaml                               #
        ##############################################################
        originalPath = dataModel + "/" + "swagger.yaml"
        message = "updated swagger.yaml"
        [ok, result] = github_delete_file_push(originalPath, repoName, message, globalUser, token)
        ##############################################################
        # remove the old new_model.yaml                              #
        ##############################################################
        originalPath = dataModel + "/" + "new_model.yaml"
        message = "removed new_model.yaml"
        [ok, result] = github_delete_file_push(originalPath, repoName, message, globalUser, token)
        ##############################################################
        # push the new swagger.yaml                                  #
        ##############################################################
        contentVariable = swaggerContent
        fileTargetPath = dataModel + "/" + "swagger.yaml"
        github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token)

