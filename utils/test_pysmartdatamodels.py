import pysmartdatamodels as sdm

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

print(sdm.list_all_datamodels())

print(sdm.list_all_subjects())

print(sdm.datamodels_subject("dataModel.Weather"))

print(sdm.description_attribute(subject, dataModel, attribute))

print(sdm.datatype_attribute(subject, dataModel, attribute))

print(sdm.model_attribute(subject, dataModel, attribute))

print(sdm.units_attribute(subject, dataModel, attribute))

print(sdm.attributes_datamodel(subject, dataModel))

print(sdm.print_datamodel(subject, dataModel, ",", [ "property", "type", "dataModel", "repoName", "description", "typeNGSI", "modelTags", "format", "units", "model", ]))

sdm.update_data()