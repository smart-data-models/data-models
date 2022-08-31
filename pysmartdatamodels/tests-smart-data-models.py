from pysmartdatamodels import *


def echo_separator(functionname):
    print()
    print("_________________________________________________")
    print()
    input(functionname)


# subject = "dataModel.Weather"
# datamodel = "WeatherObserved"
attribute = "precipitation"
subject = "dataModel.OSLO"
datamodel = "BicycleParkingStation"


# 11
echo_separator("print_datamodel(subject, datamodel, separator, meta_attributes) " + str(subject) + " " + str(datamodel))
separator = chr(9)
meta_attributes = ["property", "type", "typeNGSI", "description"]
output = print_datamodel(subject, datamodel, separator, meta_attributes)
try:
    assert "Intensity of the wind" in output
    print(output)
except AssertionError:
    print(output)
    print("error in listed at data model " + str(datamodel))


# 1
echo_separator("list_all_datamodels")
output = list_all_datamodels()

try:
    assert datamodel in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing " + str(datamodel) + " data model not present")

# 2
echo_separator("list_all_subjects")
output = list_all_subjects()
try:
    assert subject in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing " + str(subject) + " subject not present")

# 3

echo_separator("function datamodels_subject(subject) " + str(subject))
output = datamodels_subject(subject)
try:
    assert all(i in output for i in ["SeaConditions", "WeatherAlert", "WeatherForecast", "WeatherObserved"])
    print(output)
except AssertionError:
    print(output)
    print("error in listing " + str(attribute) + " description not present or wrong")

# 4

echo_separator(
    "functions description_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(
        attribute))
output = description_attribute(subject, datamodel, attribute)
try:
    assert attribute in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing " + str(subject) + " data model not present")

# 5
echo_separator(
    "datatype_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
output = datatype_attribute(subject, datamodel, attribute)
try:
    assert "number" in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing " + str(attribute) + " data type not present or wrong")

# 6
echo_separator(
    "model_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
output = model_attribute(subject, datamodel, attribute)
try:
    assert "https://schema.org/Number" in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing the model of the attribute " + str(attribute))

# 7
echo_separator(
    "units_attribute(subject, datamodel, attribute)) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
output = units_attribute(subject, datamodel, attribute)
try:
    assert "Liters per square meter" in output
    print(output)
except AssertionError:
    print(output)
    print("error in listing units of the attribute " + str(attribute))

    # 8
    echo_separator("attributes_datamodel(subject, datamodel) " + str(subject) + " " + str(datamodel))
    output = attributes_datamodel(subject, datamodel)
    try:
        attributesOutput = set(output)
        attributesSet = {"address", "airQualityIndex", "airQualityIndexForecast", "airTemperatureForecast",
                         "airTemperatureTSA", "alternateName", "aqiMajorPollutant", "aqiMajorPollutantForecast",
                         "areaServed", "atmosphericPressure", "dataProvider", "dateCreated", "dateModified",
                         "dateObserved", "description", "dewPoint", "feelLikesTemperature", "gustSpeed", "id",
                         "illuminance", "location", "name", "owner", "precipitation", "precipitationForecast",
                         "pressureTendency", "refDevice", "refPointOfInterest", "relativeHumidity",
                         "relativeHumidityForecast", "seeAlso", "snowHeight", "solarRadiation", "source",
                         "streamGauge", "temperature", "type", "uVIndexMax ", "visibility", "weatherType",
                         "windDirection", "windSpeed"}
        assert attributesSet in attributesOutput
        print(output)
    except AssertionError:
        print(output)
        print("error in listing the attributes of data model " + str(datamodel))

# 9
echo_separator( "ngsi_datatype_attribute(subject, datamodel, attribute) " + str(subject) + " " + str(datamodel) + " " + str(attribute))
output = ngsi_datatype_attribute(subject, datamodel, attribute)
try:
    assert "Property" in output
    print(output)
except AssertionError:
    print(output)
    print("error in NGSI data type at attribute " + str(attribute))

# 10
schemaUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherAlert/schema.json"
echo_separator("validate_data_model_schema(schemaUrl)")
output = validate_data_model_schema(schemaUrl)
try:
    assert "0 properties are not described at all and 0 have descriptions that must be completed" in output["schemaDiagnose"]
    print(output)
except AssertionError:
    print(output)
    print("error in schema located at " + str(schemaUrl))

