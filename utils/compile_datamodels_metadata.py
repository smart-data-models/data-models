
import json

def open_json(fileUrl):
    #function to open a json file either from a local directory or a remote web
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

# list of data models. Possibly to be used the local copy when used in pysmart datamodels package
datamodels_list_file = "https://github.com/smart-data-models/data-models/raw/master/specs/AllSubjects/official_list_data_models.json"
datamodels_list = open_json(datamodels_list_file)["officialList"]

# the output file with the contents
output_file = "datamodels_metadata.json"
output = []
limit = 3000
counter = 0
for repo in datamodels_list:
    subject = repo["repoName"]
    print(subject)
    datamodels = repo["dataModels"]
    for datamodel in datamodels:
        datamodel_object = {}
        print(datamodel)
        counter += 1
        if counter > limit:
            break
        schema_url = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + datamodel + "/schema.json"
        schema = open_json(schema_url)
        datamodel_object["subject"] = subject
        datamodel_object["dataModel"] = datamodel
        if "$schemaVersion" in schema:
            datamodel_object["version"] = schema["$schemaVersion"] 
        if "modelTags" in schema:
            datamodel_object["modelTags"] = schema["modelTags"]
        if "title" in schema:
            datamodel_object["title"] = schema["title"]
        if "$id" in schema:
            datamodel_object["$id"] = schema["$id"]
        if "description" in schema:
            datamodel_object["description"] = schema["description"]
        if "derivedFrom" in schema:
            datamodel_object["derivedFrom"] = schema["derivedFrom"]
        if "license" in schema:
            datamodel_object["license"] = schema["license"]
        if "required" in schema:
            datamodel_object["required"] = schema["required"]
        datamodel_object["yamlUrl"] = schema_url.replace("schema.json", "model.yaml")
        datamodel_object["jsonSchemaUrl"] = schema_url
        datamodel_object["@context"] = schema_url.replace(datamodel + "/schema.json", "context.jsonld")
        datamodel_object["exampleKeyvaluesJson"] = schema_url.replace("schema.json", "examples/example.json")
        datamodel_object["exampleKeyvaluesJsonld"] = schema_url.replace("schema.json", "examples/example.jsonld")
        datamodel_object["exampleNormalizedJson"] = schema_url.replace("schema.json", "examples/example-normalized.json")
        datamodel_object["exampleNormalizedJsonld"] = schema_url.replace("schema.json","examples/example-normalized.jsonld")
        datamodel_object["sql"] = schema_url.replace("schema.json", "schema.sql")
        datamodel_object["adopters"] = schema_url.replace("schema.json", "ADOPTERS.yaml")
        datamodel_object["contributors"] = schema_url.replace(datamodel + "/schema.json", "CONTRIBUTORS.yaml")

        output.append(datamodel_object)
with open(output_file, "w") as file:
    json.dump(output, file)
