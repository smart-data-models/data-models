from pysmartdatamodels import pysmartdatamodels as sdm

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

serverUrl = "https://smartdatamodels.org:1026"

value = 0.5

schemaUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.Agrifood/master/AgriApp/schema.json"

# Load all datamodels in a dict like the official list
print(sdm.load_all_datamodels())

# Load all attributes in a dict like the official export of attributes
print(len(sdm.load_all_attributes()))   # there is more than 30.000 to get all listed

# List all data models
print(sdm.list_all_datamodels())

# List all subjects
print(sdm.list_all_subjects())

# List the data models of a subject
print(sdm.datamodels_subject("dataModel.Weather"))

# List description of an attribute
print(sdm.description_attribute(subject, dataModel, attribute))

# List data-type of an attribute
print(sdm.datatype_attribute(subject, dataModel, attribute))

# Give reference model for an attribute
print(sdm.model_attribute(subject, dataModel, attribute))

# Give reference units for an attribute
print(sdm.units_attribute(subject, dataModel, attribute))

# List the attributes of a data model
print(sdm.attributes_datamodel(subject, dataModel))

# List the NGSI type (Property, Relationship or Geoproperty) of the attribute
print(sdm.ngsi_datatype_attribute(subject, dataModel, attribute))

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

# Return the links to the repositories of a data model name
print(sdm.datamodel_repolink(dataModel))

# Update the official data model list or the database of attributes from the source
# It will take a while
sdm.update_data()

# Return a fake normalized ngsi-ld format example based on the given json schema
print(sdm.ngsi_ld_example_generator(schemaUrl))

# Return a fake key value ngsi-ld format example based on the given json schema
print(sdm.ngsi_ld_keyvalue_example_generator(schemaUrl))

# Return a fake geojson feature format example based on the given json schema
print(sdm.geojson_features_example_generator(schemaUrl))

# Update a broker compliant with a specific data model, inspired by Antonio Jara
print(sdm.update_broker(dataModel, subject, attribute, value, serverUrl=serverUrl, updateThenCreate=True))