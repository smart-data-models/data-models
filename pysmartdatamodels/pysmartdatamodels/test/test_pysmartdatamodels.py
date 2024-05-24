import json
import jsonref
import requests

import sys
import os

# Get the current directory of the test file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to your package directory
package_path = os.path.dirname(current_dir)

# Add the package directory to sys.path to prioritize local import
sys.path.insert(0, package_path)

print(sys.path)
import pysmartdatamodels as sdm


repository = 'smart-data-models/data-models'  # Replace with your repository
commit_sha = '2234baefe2b6aa4debcdeabb8971a04c95b7344d'  # Replace with the desired commit SHA

def open_json(fileUrl: str):
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    open_json("https://example.com/data.json")
    {...}
    open_json("local_file.json")
    {...}
    open_json("invalid-url")
    None
    """
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

def open_jsonref(fileUrl: str):
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Capable of parsing JSON file with $ref
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    open_jsonref("https://example.com/data.json")
    {...}
    open_jsonref("local_file.json")
    {...}
    open_jsonref("invalid-url")
    None
    """
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True, merge_props=True)
            return output
        except:
            return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read(), load_on_repr=True, merge_props=True)
        except:
            return None

def test_load_all_datamodels():
    file_path = 'specs/AllSubjects/official_list_data_models.json'  # Replace with the file path
    fileUrl = f"https://raw.githubusercontent.com/{repository}/{commit_sha}/{file_path}"
    print(fileUrl)
    return open_json(fileUrl)["officialList"]

def test_load_all_attributes():
    file_path = "https://smartdatamodels.org/extra/smartdatamodels.json"
    return open_json(file_path)

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

serverUrl = "https://smartdatamodels.org:1026"

value = 0.5

schemaUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.Agrifood/master/AgriApp/schema.json"

modelYaml = "https://raw.githubusercontent.com/smart-data-models/dataModel.Transportation/master/FareCollectionSystem/model.yaml"
#
DCATAPExampleUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.DCAT-AP/master/Distribution/examples/example.json"

# Load all datamodels in a dict like the official list

# print(sdm.load_all_datamodels())
assert sdm.load_all_datamodels() == test_load_all_datamodels()

# Load all attributes in a dict like the official export of attributes
print(len(sdm.load_all_attributes()))   # there is more than 150.000 to get all listed
assert len(sdm.load_all_attributes()) == len(test_load_all_attributes())

# List all data models
print(sdm.list_all_datamodels())

# List all subjects
print(sdm.list_all_subjects())

# List the data models of a subject
print(sdm.datamodels_subject(subject))
assert sdm.datamodels_subject("dataModel.Weather") == ['SeaConditions', 'WeatherAlert', 'WeatherForecast', 'WeatherObserved']
assert sdm.datamodels_subject("dataModel.Building") == ['Building', 'BuildingOperation', 'BuildingType', 'VibrationsObserved']
assert sdm.datamodels_subject("dataModel.Nonexistentsubject") == False

# List description of an attribute
print(sdm.description_attribute(subject, dataModel, attribute))
assert sdm.description_attribute("dataModel.Weather", "WeatherForecast", "precipitation") == "Amount of water rain expected"
assert sdm.description_attribute("dataModel.Agrifood", "AgriCrop", "hasAgriSoil") == "Reference to the recommended types of soil suitable for growing this crop"
assert sdm.description_attribute("dataModel.Nonexistentsubject", "Nonexistentdatamodel", "Nonexistentattribute") == False

# List data-type of an attribute
print(sdm.datatype_attribute(subject, dataModel, attribute))
assert sdm.datatype_attribute("dataModel.Weather", "WeatherForecast", "precipitation") == "number"
assert sdm.datatype_attribute("dataModel.Environment", "NoisePollutionForecast", "noiseOrigin") == "string"
assert sdm.description_attribute("dataModel.Nonexistentsubject", "Nonexistentdatamodel", "Nonexistentattribute") == False

# Give reference model for an attribute
print(sdm.model_attribute(subject, dataModel, attribute))
assert sdm.model_attribute("dataModel.Weather", "WeatherForecast", "precipitation") == "https://schema.org/Number"
assert sdm.model_attribute("dataModel.Building", "VibrationsObserved", "accelerationMeasured") == "https://schema.org/Number"
assert sdm.model_attribute("dataModel.Parking", "OnStreetParking", "occupancyModified") == "https://schema.org/DateTime"
assert sdm.model_attribute("dataModel.Nonexistentsubject", "Nonexistentdatamodel", "Nonexistentattribute") == False

# Give reference units for an attribute
print(sdm.units_attribute(subject, dataModel, attribute))
assert sdm.units_attribute("dataModel.Weather", "WeatherForecast", "precipitation") == "Liters per square meter"
assert sdm.units_attribute("dataModel.Transportation", "TrafficFlowObserved", "averageVehicleSpeed") == "Kilometer per hour (Km/h)"
assert sdm.units_attribute("dataModel.Nonexistentsubject", "Nonexistentdatamodel", "Nonexistentattribute") == False

# List the attributes of a data model
print(sdm.attributes_datamodel(subject, dataModel))

# List the NGSI type (Property, Relationship or GeoProperty) of the attribute
print(sdm.ngsi_datatype_attribute(subject, dataModel, attribute))
assert sdm.ngsi_datatype_attribute("dataModel.Weather", "WeatherForecast", "precipitation") == "Property"
assert sdm.ngsi_datatype_attribute("dataModel.UrbanMobility", "GtfsRoute", "operatedBy") == "Relationship"
assert sdm.ngsi_datatype_attribute("dataModel.Streetlighting", "Streetlight", "location") == "GeoProperty"
assert sdm.ngsi_datatype_attribute("dataModel.Nonexistentsubject", "Nonexistentdatamodel", "Nonexistentattribute") == False

# Validate a json schema defining a data model
print(sdm.validate_data_model_schema(schemaUrl))

# Print a list of data models attributes separated by a separator
print(sdm.print_datamodel(subject, dataModel, ",", [
        "property",
        "type",
        "dataModel",
        "repoName",
        "description",
        "typeNGSI",
        "modelTags",
        "format",
        "units",
        "model",
    ]))

# Returns the link to the repository of a subject
print(sdm.subject_repolink(subject))
assert sdm.subject_repolink("dataModel.Weather") == "https://github.com/smart-data-models/dataModel.Weather.git"
assert sdm.subject_repolink("dataModel.UnmannedAerialVehicle") == "https://github.com/smart-data-models/dataModel.UnmannedAerialVehicle.git"
assert sdm.subject_repolink("dataModel.Nonexistentsubject") == False

# # Return the links to the repositories of a data model name
print(sdm.datamodel_repolink(dataModel))
assert sdm.datamodel_repolink("WeatherForecast") == ['https://github.com/smart-data-models/dataModel.Weather.git']
assert sdm.datamodel_repolink("Activity") == ['https://github.com/smart-data-models/dataModel.User.git', 'https://github.com/smart-data-models/dataModel.OCF.git']
assert sdm.datamodel_repolink("Nonexistentdatamodel") == False

# Update the official data model list or the database of attributes from the source
# It will take a while
sdm.update_data()

# Return a fake normalized ngsi-ld format example based on the given json schema
print(sdm.ngsi_ld_example_generator(schemaUrl))

# Return a fake key value ngsi-ld format example based on the given json schema
print(sdm.ngsi_ld_keyvalue_example_generator(schemaUrl))
#
# Return a fake geojson feature format example based on the given json schema
print(sdm.geojson_features_example_generator(schemaUrl))

# Update a broker compliant with a specific data model, inspired by Antonio Jara
print(sdm.update_broker(dataModel, subject, attribute, value, serverUrl=serverUrl, updateThenCreate=True))

# generates a SQL export of the structure of a data model based on the online yaml version of a data model
print(sdm.generate_sql_schema(modelYaml))

# Return the data models matching approximately a data model name
print(sdm.look_for_datamodel(dataModel))
assert sdm.look_for_datamodel(dataModel) == ['WeatherForecast']
assert sdm.look_for_datamodel(dataModel, 99) == ['WeatherForecast']
assert sdm.look_for_datamodel("WeatherFora", 84) == ['WeatherForecast']
assert sdm.look_for_datamodel("WeatherFora") == []

# Return the metadata of a data model contributors, context and specification in Spanish
print(sdm.list_datamodel_metadata(dataModel, subject))
assert sdm.list_datamodel_metadata(dataModel, subject)["contributors"] == "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/CONTRIBUTORS.yaml"
assert sdm.list_datamodel_metadata(dataModel, subject)["@context"] == "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/context.jsonld"
assert sdm.list_datamodel_metadata(dataModel, subject)["spec_ES"] == "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherForecast/doc/spec_ES.md"
assert sdm.list_datamodel_metadata("Nonexistentdatamodel", "Nonexistentsubject") == False

# Take a distribution DCAT-AP in json and validates if the downloadURL contains a valid payload against conformsTo

content_DCAT = open_jsonref(DCATAPExampleUrl)
# print(content_DCAT)
assert (sdm.validate_dcat_ap_distribution_sdm(content_DCAT) == True)
assert (sdm.validate_dcat_ap_distribution_sdm(schemaUrl) == False)


assert (sdm.subject_for_datamodel(dataModel)[0] == "dataModel.Weather")
assert (sdm.subject_for_datamodel("wrong_model") == False)