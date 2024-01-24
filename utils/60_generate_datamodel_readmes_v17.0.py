# this file will update the README of the different data models (not the subject)

# a function that with a parameter of the data model generates the contents of the README.md

import datetime
from github import Github


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


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


def read_yaml(fileUrl):
    import yaml
    from yaml.resolver import Resolver
    import re
    import requests
    # required for avoiding that No was replace by false
    for ch in "OoYyNn":
        if ch in Resolver.yaml_implicit_resolvers:
            if len(Resolver.yaml_implicit_resolvers[ch]) == 1:
                del Resolver.yaml_implicit_resolvers[ch]
            else:
                Resolver.yaml_implicit_resolvers[ch] = [x for x in Resolver.yaml_implicit_resolvers[ch]]

    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return yaml.safe_load(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return yaml.safe_load(file.read())


def craetereadme(repoName, dataModel, globalUser, token):
    # recover all the files
    notesYaml = "notes.yaml"
    g = Github(token)
    repo = g.get_organization(globalUser).get_repo(repoName)

    urlBase = "https://smart-data-models.github.io/" + repoName + "/" + dataModel
    urlSpecBase = "https://github.com/smart-data-models/" + repoName + "/blob/master/" + dataModel

    # files in root
    contents = repo.get_contents(dataModel)
    files = [i.raw_data["name"] for i in contents]

    # files in examples
    try:
        contents = repo.get_contents(dataModel + "/examples")
        files = files + ["examples/" + i.raw_data["name"] for i in contents]
    except:
        pass

    # files in docs
    try:
        contents = repo.get_contents(dataModel + "/doc")
        files = files + ["doc/" + i.raw_data["name"] for i in contents]
    except:
        pass

    schemaUrl = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/schema.json"
    schema = open_json(schemaUrl)
    print("Description : " + schema["description"])

    readmeText = "[![Smart Data Models](https://smartdatamodels.org/wp-content/uploads/2022/01/SmartDataModels_logo.png \"Logo\")](https://smartdatamodels.org)" + chr(
        10) + chr(13)
    readmeText += "# " + dataModel + chr(10)
    readmeText += "Version: " + schema["$schemaVersion"] + chr(10)
    readmeText += chr(10) + "## Description " + chr(10)
    readmeText += chr(10) + schema["description"] + chr(10)
    if "notes.yaml" in files:
        urlNotesYaml = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/" + notesYaml
        notesContent = read_yaml(urlNotesYaml)
        notesReadme = notesContent.get("notesReadme")
        if notesReadme:
            readmeText += chr(10) + notesReadme + chr(10)

    readmeText += "### Specification" + chr(10)
    if "swagger.yaml" in files:
        urlSwagger = urlBase + "/swagger.yaml"
        readmeText += chr(
            10) + "Link to the [interactive specification](https://swagger.lab.fiware.org/?url=" + urlSwagger + ")" + chr(
            10)
    if "doc/spec.md" in files:
        urlSpec = urlSpecBase + "/doc/spec.md"
        readmeText += chr(10) + "Link to the [specification](" + urlSpec + ")" + chr(10)
    if "doc/spec_ES.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_ES.md"
        readmeText += chr(10) + "Enlace a la [Especificación en español](" + urlSpec + ")" + chr(10)
    if "doc/spec_FR.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_FR.md"
        readmeText += chr(10) + "Lien vers le [spécification en français](" + urlSpec + ")" + chr(10)
    if "doc/spec_DE.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_DE.md"
        readmeText += chr(10) + "Link zur [deutschen Spezifikation](" + urlSpec + ")" + chr(10)
    if "doc/spec_IT.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_IT.md"
        readmeText += chr(10) + "Link alla [specifica](" + urlSpec + ")" + chr(10)
    if "doc/spec_JA.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_JA.md"
        readmeText += chr(10) + "[仕様へのリンク](" + urlSpec + ")" + chr(10)
    if "doc/spec_ZH.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_ZH.md"
        readmeText += chr(10) + "[链接到规范](" + urlSpec + ")" + chr(10)
    if "doc/spec_KO.md" in files:
        urlSpec = urlSpecBase + "/doc/spec_KO.md"
        readmeText += chr(10) + "[사양 링크](" + urlSpec + ")" + chr(10)

    readmeText += "### Examples" + chr(10)
    if "examples/example.json" in files:
        urlExampleKV2 = urlBase + "/examples/example.json"
        readmeText += chr(10) + "Link to the [example](" + urlExampleKV2 + ") (keyvalues) for NGSI v2" + chr(10)
    if "examples/example.jsonld" in files:
        urlExampleKVLD = urlBase + "/examples/example.jsonld"
        readmeText += chr(10) + "Link to the [example](" + urlExampleKVLD + ") (keyvalues) for NGSI-LD" + chr(10)
    if "examples/example-normalized.json" in files:
        urlExampleNV2 = urlBase + "/examples/example-normalized.json"
        readmeText += chr(10) + "Link to the [example](" + urlExampleNV2 + ") (normalized) for NGSI-V2" + chr(10)
    if "examples/example-normalized.jsonld" in files:
        urlExampleNLD = urlBase + "/examples/example-normalized.jsonld"
        readmeText += chr(10) + "Link to the [example](" + urlExampleNLD + ") (normalized) for NGSI-LD" + chr(10)
    if "examples/example-geojsonfeature.json" in files:
        urlExampleGeo = urlBase + "/examples/example-geojsonfeature.json"
        readmeText += chr(10) + "Link to the [example](" + urlExampleGeo + ") (geojson feature) for NGSI-LD" + chr(10)
    # csv files
    if "examples/example.json.csv" in files:
        urlExampleKV2CSV = urlSpecBase + "/examples/example.json.csv"
        readmeText += chr(
            10) + "Link to the [example](" + urlExampleKV2CSV + ") (keyvalues) for NGSI v2 in CSV format" + chr(10)
    if "examples/example.jsonld.csv" in files:
        urlExampleKVLDCSV = urlSpecBase + "/examples/example.jsonld.csv"
        readmeText += chr(
            10) + "Link to the [example](" + urlExampleKVLDCSV + ") (keyvalues) for NGSI-LD in CSV format" + chr(10)
    if "examples/example-normalized.json.csv" in files:
        urlExampleNV2CSV = urlSpecBase + "/examples/example-normalized.json.csv"
        readmeText += chr(
            10) + "Link to the [example](" + urlExampleNV2CSV + ") (normalized) for NGSI-V2 in CSV format" + chr(10)
    if "examples/example-normalized.jsonld.csv" in files:
        urlExampleNLDCSV = urlSpecBase + "/examples/example-normalized.jsonld.csv"
        readmeText += chr(
            10) + "Link to the [example](" + urlExampleNLDCSV + ") (normalized) for NGSI-LD in CSV format" + chr(10)

    readmeText += "### Dynamic Examples generation" + chr(10)
    if "schema.json" in files:
        urlNGSILDExample = "https://smartdatamodels.org/extra/ngsi-ld_generator.php?schemaUrl=https://raw.githubusercontent.com/smart-data-models/" + repoName + "/" + "master" + "/" + dataModel + "/" + "schema.json" + "&email=info@smartdatamodels.org"
        urlNGSILDExampleKeyvalues = "https://smartdatamodels.org/extra/ngsi-ld_generator_keyvalues.php?schemaUrl=https://raw.githubusercontent.com/smart-data-models/" + repoName + "/" + "master" + "/" + dataModel + "/" + "schema.json" + "&email=info@smartdatamodels.org"
        urlGeojsonFeatures = "https://smartdatamodels.org/extra/geojson_features_generator.php?schemaUrl=https://raw.githubusercontent.com/smart-data-models/" + repoName + "/" + "master" + "/" + dataModel + "/" + "schema.json" + "&email=info@smartdatamodels.org"

        readmeText += chr(
            10) + "Link to the [Generator](" + urlNGSILDExample + ") of NGSI-LD normalized payloads compliant with this data model. Refresh for new values" + chr(
            10)
        readmeText += chr(
            10) + "Link to the [Generator](" + urlNGSILDExampleKeyvalues + ") of NGSI-LD keyvalues payloads compliant with this data model. Refresh for new values" + chr(
            10)
        readmeText += chr(
            10) + "Link to the [Generator](" + urlGeojsonFeatures + ") of geojson feature format payloads compliant with this data model. Refresh for new values" + chr(
            10)

    readmeText += "### PostgreSQL schema" + chr(10)
    if "schema.sql" in files:
        urlschemaSQL = urlSpecBase + "/schema.sql"
        readmeText += chr(10) + "Link to the [PostgreSQL schema](" + urlschemaSQL + ") of this data model" + chr(10)

    readmeText += "### Contribution" + chr(10)
    urlIssue = "https://github.com/smart-data-models/" + repoName + "/issues"
    urlPull = "https://github.com/smart-data-models/" + repoName + "/pulls"
    urlContributionManual = "https://bit.ly/contribution_manual"
    urlTest = "https://smartdatamodels.org/index.php/data-models-contribution-api/"
    urlSQLGen = "https://smartdatamodels.org/index.php/sql-service/"

    readmeText += chr(
        10) + " If you have any issue on this data model you can raise an [issue](" + urlIssue + ")  or contribute with a [PR](" + urlPull + ")" + chr(
        10)

    readmeText += chr(
        10) + " If you wish to develop your own data model you can start from [contribution manual](" + urlContributionManual + "). Several services have been developed to help with: "
    readmeText += chr(
        10) + " - [Test data model repository](" + urlTest + ") including the schema and example payloads, etc"
    readmeText += chr(
        10) + " - [Generate PostgreSQL schema](" + urlSQLGen + ") to help create a table, create type, etc"
    return readmeText


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


#########################################################
# Static parameters for generation                      #
#########################################################
#                                                       #

credentialsFile = "/home/fiware/credentials.json"
# credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
credentials = open_json(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
g = Github(token)

currentDT = datetime.datetime.now()
updatingDate = currentDT.isoformat()

#                                                       #
#########################################################

#########################################################
# Filter to select data models                          #
#########################################################
#                                                       #

configFile = "datamodels_to_publish.json"
dataModelsToPublish = open_json(configFile)
repoName = dataModelsToPublish["subject"]
dataModels = dataModelsToPublish["dataModels"]

echo("subject", repoName)
echo("dataModels", dataModels)
echo("filter or no ", dataModelsToPublish["filterDataModels"])
echo("languages ", dataModelsToPublish["languages"])

#                                                       #
#########################################################
if isinstance(dataModels, str):
    dataModels = [dataModels]
for dataModel in dataModels:
    markdown = craetereadme(repoName, dataModel, globalUser, token)
    message = "updated on " + str(updatingDate)
    github_push_from_variable(markdown, repoName, dataModel + "/README.md", message, globalUser, token)
