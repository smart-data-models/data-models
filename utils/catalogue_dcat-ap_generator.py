from pysmartdatamodels import pysmartdatamodels as sdm
import time
from datetime import datetime
import json

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


catalogue_file = "catalogue.json"
metadata_file = "datamodels_metadata.json"
global metadata
metadata = open_json(metadata_file)
def find_dict(subject, datamodel, metadata_):
    subject_array = [element for element in metadata_ if element["subject"] == subject]
    # print("subject array for data model " + datamodel)
    # print(subject_array)
    for item in subject_array:
        # print(item)
        if item["dataModel"] == datamodel:
            return item
        else:
            print("not found " + subject + " data model " + datamodel)
    return False

catalogue = {}  

catalogue["title"] ="The Smart Data Models iniative catalogue"
catalogue["description"] = "This is the list in DCAT-AP 2.1.1 estandar of the Smart Data Models catalogue"
catalogue["homepage"] = "https://smartdatamodels.org/index.php"
catalogue["license"] = "Creative Commons BY International 4.0"
catalogue["publisher"] = "The Smart Data Models initiative "
timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
catalogue["issued"] = timestamp
catalogue["modified"] = timestamp
catalogue["creator"] = "The Smart Data Models initiative "
catalogue["dataset"] = []
subjects = sdm.list_all_subjects()
offset = 0

limit = 1000
counter = 0
for subject in subjects:
    datamodels = sdm.datamodels_subject(subject)
    for index, datamodel in enumerate(datamodels):
        counter += 1
        if counter > limit:
            break
        subjectRoot = sdm.subject_repolink(subject)
        dataset_object = {}
        dataset_object["landingPage"] = subjectRoot.replace(".git", "/" + datamodel + "/README.md")
        metadata_datamodel = find_dict(subject, datamodel, metadata)
        print(metadata_datamodel)
        dataset_object["identifier"] = metadata_datamodel["$id"]
        dataset_object["title"] = metadata_datamodel["title"]
        dataset_object["description"] = metadata_datamodel["description"]
        dataset_object["publisher"] = "The Smart Data Models initiative"
        dataset_object["hasVersion"] = []
        # populating the schema
        distribution_object = {}
        distribution_object["versionInfo"] = metadata_datamodel["version"]
        distribution_object["landingPage"] = dataset_object["landingPage"]
        distribution_object["identifier"] = dataset_object["identifier"]
        distribution_object["title"] = dataset_object["title"]
        distribution_object["format"] = "json schema"
        distribution_object["mediaType"] = "application / schema + json"
        distribution_object["accessURL"] = metadata_datamodel["jsonSchemaUrl"]
        dataset_object["hasVersion"].append(distribution_object)

        # populating the yaml
        distribution_object = {}
        distribution_object["versionInfo"] = metadata_datamodel["version"]
        distribution_object["landingPage"] = dataset_object["landingPage"]
        distribution_object["identifier"] = metadata_datamodel["jsonSchemaUrl"]
        distribution_object["title"] = dataset_object["title"]
        distribution_object["format"] = "yaml"
        distribution_object["mediaType"] = "application/x-yaml"
        distribution_object["accessURL"] = metadata_datamodel["yamlUrl"]
        dataset_object["hasVersion"].append(distribution_object)

        catalogue["dataset"].append(dataset_object)
    offset = offset + index
    print(catalogue)
with open(catalogue_file , "w") as file:
    file.write(str(json.dumps(catalogue, indent=4)))





payload = {
    "title": "Smart Data Models: Energy",
    "description": "domain specific data models related to energy. The adaptation of IEC standards (CIM) is one of the goals of this subject.",
    "homepage": "https://smartdatamodels.org/index.php/category/energy/",
    "publisher": {
        "name": "https://smartdatamodels.org/"
    },
    "dataset": [
        {
            "landingPage": "https://github.com/smart-data-models/dataModel.Energy/blob/master/ACMeasurement/README.md",
            "identifier": "//TODO (mandatory)",
            "title": "ACMeasurement",
            "description": "The Data Model intended to measure the electrical energies consumed by an electrical system which uses an Alternating Current (AC) for a three-phase (L1, L2, L3) or single-phase (L) and neutral (N).",
            "publisher": {
                "name": "https://smartdatamodels.org/"
            },
            "hasVersion": [
                {
                    "versionNotes": {},
                    "versionInfo": "0.0.1",
                    "issued": "//TODO (optional)",
                    "landingPage": "https://github.com/smart-data-models/dataModel.Energy/blob/master/ACMeasurement/README.md",
                    "identifier": "//TODO (mandatory)",
                    "title": "ACMeasurement V0.0.1",
                    "description": "The Data Model intended to measure the electrical energies consumed by an electrical system which uses an Alternating Current (AC) for a three-phase (L1, L2, L3) or single-phase (L) and neutral (N). It integrates the initial version of the data Modem [THREEPHASEMEASUREMENT], extended to also perform single-phase measurements. It includes attributes for various electrical measurements such as power, frequency, current and voltage.",
                    "distribution": [
                        {
                            "accessURL": "https://raw.githubusercontent.com/smart-data-models/dataModel.Energy/master/ACMeasurement/schema.json",
                            "title": "schema.json",
                            "format": "JSON",
                            "description": "JSON schema serialization of the data model.",
                            "mediaType": "application/schema+json"
                        },
                        {
                            "accessURL": "https://raw.githubusercontent.com/smart-data-models/dataModel.Energy/master/ACMeasurement/model.yaml",
                            "title": "model.yaml",
                            "format": "JSON",
                            "description": "Yaml serialization of the data model.",
                            "mediaType": "application/schema+json"
                        }
                    ]
                }
            ]
        }
    ]
}
