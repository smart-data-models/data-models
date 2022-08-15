from pysmartdatamodels.pysmartdatamodels import *


def echo_separator(functionname):
    print()
    print("_________________________________________________")
    print()
    input(functionname)

# 1
echo_separator("list_all_datamodels")
print(list_all_datamodels())

# 2
echo_separator("list_all_subjects")
print(list_all_subjects())

# 3
subject = "dataModel.Weather"
echo_separator("function datamodels_subject(subject) " + str(subject))
print(datamodels_subject(subject))

# 4
datamodel = "WeatherObserved"
attribute = "precipitation"
echo_separator("functions description_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
print(description_attribute(subject, datamodel, attribute))

# 5
echo_separator("datatype_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
print(datatype_attribute(subject, datamodel, attribute))

# 6
echo_separator("model_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
print(model_attribute(subject, datamodel, attribute))

# 7
echo_separator("units_attribute(subject, datamodel, attribute)) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
print(units_attribute(subject, datamodel, attribute))


# 8
echo_separator("attributes_datamodel(subject, datamodel) " + str(subject) + " " + str(datamodel))
print(attributes_datamodel(subject, datamodel))

# 9
echo_separator("ngsi_datatype_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
print(ngsi_datatype_attribute(subject, datamodel, attribute))


# 10
schemaUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherAlert/schema.json"
echo_separator("validate_data_model_schema(schemaUrl)")
print(validate_data_model_schema(schemaUrl))
