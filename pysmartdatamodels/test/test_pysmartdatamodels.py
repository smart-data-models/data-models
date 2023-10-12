from pysmartdatamodels import pysmartdatamodels as sdm

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

serverUrl = "https://smartdatamodels.org:1026"

value = 0.5

schemaUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.Agrifood/master/AgriApp/schema.json"

modelYaml = "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherAlert/model.yaml"

print(sdm.load_all_datamodels())

print(len(sdm.load_all_attributes())) # there is more than 21.000 to get all listed

print(sdm.list_all_datamodels())

print(sdm.list_all_subjects())

print(sdm.datamodels_subject("dataModel.Weather"))

print(sdm.description_attribute(subject, dataModel, attribute))

print(sdm.datatype_attribute(subject, dataModel, attribute))

print(sdm.model_attribute(subject, dataModel, attribute))

print(sdm.units_attribute(subject, dataModel, attribute))

print(sdm.attributes_datamodel(subject, dataModel))

print(sdm.ngsi_datatype_attribute(subject, dataModel, attribute))

print(sdm.print_datamodel(subject, dataModel, ",", [ "property", "type", "dataModel", "repoName", "description", "typeNGSI", "modelTags", "format", "units", "model", ]))

print(sdm.subject_repolink(subject))

print(sdm.datamodel_repolink(dataModel))

sdm.update_data()

print(sdm.ngsi_ld_example_generator(schemaUrl))

print(sdm.ngsi_ld_keyvalue_example_generator(schemaUrl))

print(sdm.geojson_features_example_generator(schemaUrl))

print(sdm.update_broker(dataModel, subject, attribute, value, serverUrl=serverUrl))

print(sdm.generate_sql_schema(modelYaml))