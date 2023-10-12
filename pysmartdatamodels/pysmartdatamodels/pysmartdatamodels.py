import datetime
import json
import os
import sys
import urllib.request

import jsonschema
import pytz
import requests
from jsonschema import validate
from .utils import (create_context, extract_datamodel_from_raw_url,
                    extract_subject_from_raw_url, generate_random_string,
                    normalized2keyvalues, open_jsonref, open_yaml, parse_property)


path = __file__

# Find the index of the last occurrence of /
index = path.rfind(os.sep)

# Extract the right part of the string up until the last /
left_part = path[:index]
# lookup install path for - model-assets

official_list_file_name = left_part + "/model-assets/official_list_data_models.json"
ddbb_attributes_file = left_part + "/model-assets/smartdatamodels.json"

# data models that are not able to generate examples from the schema due to certain issue
issue_datamodels = ["SeaportFacilities", "OffStreetParking", "OnStreetParking", "ParkingGroup", "WeatherAlert", "Museum", "MosquitoDensity", "Alert", "MediaEvent",  "DataResourceFrictionlessData", "TableSchemaFrictionlessData", "free_bike_status", "geofencing_zones", "station_information", "station_status", "system_alerts", "Presentation", "DigitalInnovationHub"]
issue_message = "====== The specific models are still pending ====== \nWe cannot generate examples from it now due to some inner problems of the data model scheme json file"

# 1
def load_all_datamodels():
    """Returns a dict with all data models with this object structure
        - repoName: The name of the subject
        - repoLink: the link to the repository of the subject
        - dataModels: An array with all the datamodels of this subject
        - domains: an array to the domains that this subject belongs to
        Parameters:

        Returns:
           array of objects with the description of the subject
        """
    import json

    output = []
    # Opens the file with the list of data models
    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        output = json.load(list_of_datamodels_pointer)["officialList"]
    return output

# 2
def load_all_attributes():
    """Returns an array of objects describing every attribute in the data models
        - _id: identifier of the item
        - property: the name of the attribute
        - dataModel: the data model this attribute is present
        - repoName: the subject this data model belongs to
        - description: the description of the attribute
        - typeNGSI: Whether it is a property, Geoproperty, or relationship
        - modelTags: inherited from the data model tags
        - license: link to the license for the data model
        - schemaVersion: version of the data model
        - type: data type
        - model: when available the reference model for the attribute
        - units: when available the recommended units for the attribute
        - format: either date, or time, or date-time, or URI, etc the format of the attribute
    Parameters:

    Returns:
        array of objects with the description of the subject
    """

    output = []
    # Opens the file with the list of data models
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_file_pointer:
        output = json.load(ddbb_attributes_file_pointer)
    return output

# 3
def list_all_datamodels():
    """List the names of the entities defined in the data models.
    Parameters:

    Returns:
       array of strings: data models' names
    """

    output = []
    # Opens the file with the list of data models
    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        # Loads it in the dictionary
        print(official_list_file_name)
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        # Stores it in the output variable
        for item in datamodelsdict:
            for datamodel in item["dataModels"]:
                output.append(datamodel)

    return output


# 4
def list_all_subjects():
    """List the names of the subjects (groups of data models). The subject's names define repositories with the name dataModel.subject at the root of the https://smart-data-models.github.com site
    Parameters:

    Returns:
       array of strings: subjects' names
    """

    output = []

    # Opens the file with the list of data models
    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        for item in datamodelsdict:
            output.append(item["repoName"])

    return output


# 5
def datamodels_subject(subject: str):
    """List the names of the entities defined in the data models.
    Parameters:
        subject: name of the subject

    Returns:
        if subject is found
            array of strings: data models' names belonging to the subject
        if subject is not found
            False
    """

    output = []
    done = False

    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        for item in datamodelsdict:
            if "repoName" and "dataModels" in item:
                if item["repoName"] == subject:
                    output = item["dataModels"]
                    done = True
    if not done:
        output = False

    return output


# 6
def description_attribute(subject, datamodel, attribute):
    """List the description of an attribute belonging to a subject and data model.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        attribute: name of the attribute

    Returns:
        if subject, datamodel and attribute are found
            string: attribute's description
        if any of the input parameters is not found
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (
                (item["repoName"] == subject)
                and (item["dataModel"] == datamodel)
                and (item["property"] == attribute)
            ):
                output = item["description"]
                done = True
        except:
            nada = 0
    else:
        if not done:
            output = False

    return output


# 7
def datatype_attribute(subject, datamodel, attribute):
    """List the data type of an attribute belonging to a subject and data model.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        attribute: name of the attribute

    Returns:
        if subject, datamodel and attribute are found
            string: attribute's data type
        if any of the input parameters is not found
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (
                (item["repoName"] == subject)
                and (item["dataModel"] == datamodel)
                and (item["property"] == attribute)
            ):
                if "type" in item:
                    output = item["type"]
                    done = True
                else:
                    output = False
                    done = True
        except:
            nada = 0
    else:
        if not done:
            output = False

    return output


# 8
def model_attribute(subject, datamodel, attribute):
    """List the model of an attribute (when available) belonging to a subject and data model.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        attribute: name of the attribute

    Returns:
        if subject, datamodel and attribute are found
            string: attribute model's URL
        if any of the input parameters is not found or there is not a model
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (
                (item["repoName"] == subject)
                and (item["dataModel"] == datamodel)
                and (item["property"] == attribute)
            ):
                if "model" in item:
                    output = item["model"]
                    done = True
                else:
                    output = False
                    done = True
        except:
            nada = 0
    else:
        if not done:
            output = False

    return output


# 9
def units_attribute(subject, datamodel, attribute):
    """List the recommended units of an attribute belonging to a subject and data model.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        attribute: name of the attribute

    Returns:
        if subject, datamodel and attribute are found
            string: acronym/text of the recommended units
        if any of the input parameters is not found or there are not recommended units
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (
                (item["repoName"] == subject)
                and (item["dataModel"] == datamodel)
                and (item["property"] == attribute)
            ):
                if "units" in item:
                    output = item["units"]
                    done = True
                else:
                    output = False
                    done = True
        except:
            nada = 0
    else:
        if not done:
            output = False

    return output


# 10
def attributes_datamodel(subject, datamodel):
    """List the attributes of a data model (currently only first level ones) .
    Parameters:
        subject: name of the subject
        datamodel: name of the data model

    Returns:
        if subject and datamodel  are found
            array: attribute's names
        if any of the input parameters is not found
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (item["repoName"] == subject) and (item["dataModel"] == datamodel):
                if "property" in item:
                    output.append(item["property"])
                    done = True
        except:
            nada = 0
    else:
        if len(output) < 1:
            output = False
        if not done:
            output = False

    return output


# 11
def ngsi_datatype_attribute(subject, datamodel, attribute):
    """List the NGSI data type of an attribute (Property, Relationship or Geoproperty) belonging to a subject and data model.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        attribute: name of the attribute

    Returns:
        if subject, datamodel and attribute are found
            string: NGSI data type
        if any of the input parameters is not found
            False
    """

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
        # print(item)
        try:
            if (
                (item["repoName"] == subject)
                and (item["dataModel"] == datamodel)
                and (item["property"] == attribute)
            ):
                if "typeNGSI" in item:
                    output = item["typeNGSI"]
                    done = True
        except:
            nada = 0

    if done:
        return output
    else:
        return False

# 12
def validate_data_model_schema(schema_url):
    """Validates a json schema defining a data model.
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json


    Returns:
        object with four elements:
        - documentationStatusofProperties: For each first level attribute lists if the attribute is documented and includes the description (when available). Also the NGSI type if is set and which one is described.
          Example:
            "dateCreated":
                  {
                  "x-ngsi": true,
                  "x-ngsi_text": "ok to Property",
                  "documented": true,
                  "text": "This will usually be allocated by the storage platform.. Entity creation timestamp"
                  },
        - schemaDiagnose: It counts the attributes with right descriptions and those which don't.
        - alreadyUsedProperties: It identifies attributes that have already been used in other data models and includes their definition
        - availableProperties: Identifies those attributes which are not already included in any other data model
    """

    def order_dictionary(dictionary):
        # This function return the same dictionary but ordered by its keys
        import collections

        if isinstance(dictionary, dict):
            od = collections.OrderedDict(sorted(dictionary.items()))
            return od
        else:
            return dictionary

    def exist_page(url):
        import requests

        output = []
        try:
            pointer = requests.get(url)
            if pointer.status_code == 200:
                return [True, pointer.text]
            else:
                return [False, pointer.status_code]
        except:
            return [False, "wrong domain"]

    def parse_payload(schemaPayload, level):
        output = {}
        if "allOf" in schemaPayload:
            # echo("allOf level", level)
            for index in range(len(schemaPayload["allOf"])):
                # echo("passing to next level this payload=", str(schemaPayload["allOf"][index]))
                partialOutput = parse_payload(schemaPayload["allOf"][index], level + 1)
                output = dict(output, **partialOutput)
        if "anyOf" in schemaPayload:
            # echo("anyOf level", level)
            for index in range(len(schemaPayload["anyOf"])):
                # echo("original output", output)
                partialOutput = parse_payload(schemaPayload["anyOf"][index], level + 1)
                # echo("parsed anyOf", partialOutput)
                output = dict(output, **partialOutput)
                # echo("current output", output)
        if "properties" in schemaPayload:
            # echo("properties level", level)
            for prop in schemaPayload["properties"]:
                # echo(" dealing at level " + str(level) + " with prop=", prop)
                if "allOf" in prop:
                    # echo("original output", output)
                    # echo("parsed allOf", partialOutput)
                    output[prop] = parse_payload(
                        schemaPayload["properties"]["allOf"], level + 1
                    )
                elif "anyOf" in prop:
                    # echo("original output", output)
                    # echo("parsed anyOf", partialOutput)
                    output[prop] = parse_payload(
                        schemaPayload["properties"]["anyOf"], level + 1
                    )
                else:
                    # echo("parsing this payload at " + str(level) + " from prop =" + prop, schemaPayload["properties"][prop])
                    try:
                        output[prop]
                    except:
                        output[prop] = {}
                    for item in list(schemaPayload["properties"][prop]):
                        # echo("parsing at level " + str(level) + " item= ", item)

                        if item == "description":
                            # print("Detectada la descripcion de la propiedad=" + prop)
                            separatedDescription = str(
                                schemaPayload["properties"][prop]["description"]
                            ).split(". ")
                            copiedDescription = list.copy(separatedDescription)
                            # print(copiedDescription)
                            for descriptionPiece in separatedDescription:
                                if descriptionPiece in propertyTypes:
                                    # print(descriptionPiece)
                                    try:
                                        output[prop]["x-ngsi"]["type"] = descriptionPiece
                                    except:
                                        output[prop]["x-ngsi"]["type"] = {}
                                        output[prop]["x-ngsi"]["type"] = descriptionPiece
                                    copiedDescription.remove(descriptionPiece)
                                    # print(schemaPayload["properties"][prop])
                                elif descriptionPiece.find("Model:") > -1:
                                    # print(descriptionPiece)
                                    copiedDescription.remove(descriptionPiece)
                                    # print(copiedDescription)
                                    try:
                                        output[prop]["x-ngsi"][
                                            "model"
                                        ] = descriptionPiece.replace("'", "").replace(
                                            "Model:", ""
                                        )
                                    except:
                                        output[prop]["x-ngsi"] = {}
                                        output[prop]["x-ngsi"][
                                            "model"
                                        ] = descriptionPiece.replace("'", "").replace(
                                            "Model:", ""
                                        )

                                elif descriptionPiece.find("Units:") > -1:
                                    # print(descriptionPiece)
                                    copiedDescription.remove(descriptionPiece)
                                    # print(copiedDescription)
                                    try:
                                        output[prop]["x-ngsi"][
                                            "units"
                                        ] = descriptionPiece.replace("'", "").replace(
                                            "Units:", ""
                                        )
                                    except:
                                        output[prop]["x-ngsi"] = {}
                                        output[prop]["x-ngsi"][
                                            "units"
                                        ] = descriptionPiece.replace("'", "").replace(
                                            "Units:", ""
                                        )
                            # print("---")
                            description = ". ".join(copiedDescription)
                            output[prop][
                                "description"
                            ] = description  # the remaining part of the description is used

                        elif item == "type":
                            output[prop]["type"] = schemaPayload["properties"][prop][
                                "type"
                            ]
                        else:
                            # echo("parsing prop", prop)
                            # echo("payload", schemaPayload["properties"][prop][item])
                            output[prop][item] = schemaPayload["properties"][prop][item]
            return output
        else:
            return output

    # initialize variables for the script
    output = {}  # the json answering the test
    tz = pytz.timezone("Europe/Madrid")
    # metaSchema = open_jsonref("https://json-schema.org/draft/2019-09/hyper-schema")
    metaSchema = open_jsonref("https://json-schema.org/draft/2020-12/meta/validation")
    propertyTypes = ["Property", "Relationship", "Geoproperty"]
    incompleteDescription = "Incomplete description"
    withoutDescription = "No description at all"

    # validate inputs
    existsSchema = exist_page(schema_url)

    # url provided is an existing url
    if not existsSchema[0]:
        output["result"] = False
        output["cause"] = "Cannot find the schema at " + schema_url
        output["time"] = str(datetime.datetime.now(tz=tz))
        print(json.dumps(output))
        sys.exit()

    # url is actually a json
    try:
        schemaDict = json.loads(existsSchema[1])
    except ValueError:
        output["result"] = False
        output["cause"] = "Schema " + schema_url + " is not a valid json"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url: ": schema_url}
        print(json.dumps(output))
        sys.exit()

    # test that it is a valid schema against the metaschema
    try:
        schema = open_jsonref(schema_url)
        # echo("len of schema", len(str(schema)))
        # echo("schema", schema)
        if not bool(schema):
            output["result"] = False
            output["cause"] = "json schema returned empty (wrong $ref?)"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schema_url: ": schema_url}
            print(json.dumps(output))
            sys.exit()

    except:
        output["result"] = False
        output["cause"] = "json schema cannot be fully loaded"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        sys.exit()

    try:
        validate(instance=schema, schema=metaSchema)
    except jsonschema.exceptions.ValidationError as err:
        # print(err)
        output["result"] = False
        output["cause"] = "schema does not validate as a json schema"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        output["errorSchema"] = str(err)
        print(json.dumps(output))
        sys.exit()

    # extract properties' definitions
    # check if they are populated

    documented = "documentationStatusOfProperties"
    try:
        yamlDict = parse_payload(schema, 1)
    except:
        output["result"] = False
        output["cause"] = "schema cannot be loaded (possibly invalid $ref)"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        sys.exit()
    # echo("yamlDict", yamlDict)
    output[documented] = {}
    for key in yamlDict:
        # print(key)
        # print(yamlDict[key])
        if key != "id":
            try:
                propertyType = yamlDict[key]["type"]
                if propertyType in propertyTypes:
                    # print(propertyType)
                    # print(propertyTypes)
                    output[documented][key] = {}
                    output[documented][key]["x-ngsi"] = True
                    output[documented][key]["x-ngsi_text"] = "ok to " + str(
                        propertyType
                    )
                else:
                    output[documented][key]["x-ngsi"] = False
                    output[documented][key]["x-ngsi_text"] = (
                        "Missing any of"
                        + str(propertyTypes)
                        + " in the description of the property"
                    )
            except:
                output[documented][key] = {}
                output[documented][key]["x-ngsi"] = False
                output[documented][key]["x-ngsi_text"] = (
                    "Missing any of"
                    + str(propertyTypes)
                    + " in the description of the property"
                )

            # checking the pure description
            try:
                description = yamlDict[key]["description"]
                if len(description) > 10:
                    output[documented][key]["documented"] = True
                    output[documented][key]["text"] = description
                else:
                    output[documented][key]["documented"] = False
                    output[documented][key]["text"] = incompleteDescription
            except:
                output[documented][key] = {}
                output[documented][key]["documented"] = False
                output[documented][key]["text"] = withoutDescription
    allProperties = 0
    documentedProperties = 0
    faultyDescriptionProperties = 0
    notDescribedProperties = 0
    for key in output[documented]:
        allProperties += 1
        # print(output["properties"][key]["documented"])
        if output[documented][key]["documented"]:
            documentedProperties += 1
        elif output[documented][key]["text"] == incompleteDescription:
            faultyDescriptionProperties += 1
        elif output[documented][key]["text"] == withoutDescription:
            notDescribedProperties += 1

    output["schemaDiagnose"] = (
        "This schema has "
        + str(allProperties)
        + " properties. "
        + str(notDescribedProperties)
        + " properties are not described at all and "
        + str(faultyDescriptionProperties)
        + " have descriptions that must be completed. "
        + str(allProperties - faultyDescriptionProperties - notDescribedProperties)
        + " are described but you can review them anyway. "
    )

    # now it checks if these properties already exist in the database

    # print(json.dumps(output))
    # return json.dumps(output)
    return output


# 13 print data models attributes
def print_datamodel(subject, datamodel, separator, meta_attributes):
    """print the different elements of the attributes of a data model separated by a given separator.
    Parameters:
        subject: name of the subject
        datamodel: name of the data model
        separator: string between the different elements printed
        meta_attributes: list of different qualifiers of an attribute
             property: the name of the attribute
             type: the data type of the attribute (json schema basic types)
             dataModel: the data model the attribute belongs to
             repoName: the subject the attribute belongs to
             description: the definition of the attribute
             typeNGSI: the NGSI type, Property, Relationship or Geoproperty
             modelTags: the tags assigned to the data model
             format: For those attributes having it the format, i.e. date-time
             units: For those attributes having it the recommended units, i.e. meters
             model: For those attributes having it the reference model, i.e. https://schema.org/Number

    Returns:
        It prints a version of the attributes separated by the separator listing the meta_attributes specified
        A variable with the same strings
        if any of the input parameters is not found it returns false
            False
    """

    output = []
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)

    # available metadata in the list
    validmetadata = [
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
    ]
    defaultmetadata = ["property", "type", "typeNGSI", "description"]
    newline = chr(13) + chr(10)
    with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
        datamodelsdict = json.load(ddbb_attributes_pointer)
    print(datamodelsdict[0])
    selectedattributes = []
    for d in datamodelsdict:
        print(d)
        if "dataModel" in d and "repoName" in d:
            if d["dataModel"] == datamodel and d["repoName"] == subject:
                selectedattributes.append(d)
    # checks that there are any attribute for the data model
    if len(selectedattributes) < 1:
        return False
    else:
        if all([d in validmetadata for d in meta_attributes]):
            listedmetadata = meta_attributes
        else:
            listedmetadata = defaultmetadata
        # first line with the names of the meta data of the attributes
        output = str(separator.join(listedmetadata)) + newline

        # for every attribute in the data model
        for item in selectedattributes:
            print("item:" + str(item))

            try:
                # if all metadata are available for the attribute it is done in one shot
                selectedmeta = [item[d] for d in listedmetadata]
                print("selectedmeta:" + str(selectedmeta))
                row = separator.join(selectedmeta)
                print("row:" + str(row))
            except:
                # if all metadata are not available for the attribute it is done with a loop
                print("error")
                rowitems = []
                for d in listedmetadata:
                    if d in item:
                        rowitems.append(item[d])
                    else:
                        rowitems.append("")
                row = separator.join(rowitems)
            output += row + newline
    print(output)
    return output


#14
def subject_repolink(subject: str):
    """It returns the direct link to the repository of the subject if it is found and False if not .
    Parameters:
        subject: name of the subject

    Returns:
        if subject is found
            url of the github repository. Example for subject User it returns 'https://github.com/smart-data-models/dataModel.User.git'
        if subject is not found
            False
    """

    # output = []
    done = False

    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        for item in datamodelsdict:
            if "repoName" and "dataModels" in item:
                if item["repoName"] == subject:
                    output = item["repoLink"]
                    done = True
    if not done:
        output = False

    return output

# 15
def datamodel_repolink(datamodel: str):
    """It returns an array with the direct links to the repositories where is located the data model if it is found and False if not found.
    Parameters:
        datamodel: name of the data model

    Returns:
        if data model is found
            array of urls (even with one single result) to the github repository. Example for subject Activity it returns ['https://github.com/smart-data-models/dataModel.User.git']
        if data model is not found
            False
    """

    output = []
    done = False

    with open(official_list_file_name, "r", encoding='utf-8') as list_of_datamodels_pointer:
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        for item in datamodelsdict:
            if "repoName" and "dataModels" in item:
                dataModels = item["dataModels"]
                if datamodel in dataModels:
                    output.append(item["repoLink"])
                    done = True
    if not done:
        output = False

    return output

# 16
def update_data():
    """Download the latest data files from a remote server
    """

    data_dir = os.path.join(os.path.dirname(__file__), "model-assets")

    # Download the latest data files from a remote server
    urllib.request.urlretrieve("https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json", os.path.join(data_dir, "official_list_data_models.json"))
    urllib.request.urlretrieve("https://smartdatamodels.org/extra/smartdatamodels.json", os.path.join(data_dir, "smartdatamodels.json"))

    # Update the data files with the latest information
    # (This will depend on the specific data files and the format they use)

# 17
def ngsi_ld_example_generator(schema_url: str):
    """It returns a fake normalized ngsi-ld format example based on the given json schema
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json

    Returns:
        if the input parameter exists and the json schema is a valide json:
            a fake normalized ngsi-ld format example stored in dictionary format
        if there's any problem related to input parameter and json schema:
            False
    """

    dataModel = extract_datamodel_from_raw_url(schema_url)
    subject = extract_subject_from_raw_url(schema_url)
    if dataModel == "dataModel" or subject == "subject": return False
    if dataModel in issue_datamodels: return issue_message

    #echo("schema_url",schema_url)
    payload = open_jsonref(schema_url)
    if payload == "": return False

    # print(payload["allOf"])
    output = {}
    fullDict = {}
    # echo("payload", payload)
    if "allOf" in payload:
        for index in range(len(payload["allOf"])):
            if "properties" in payload["allOf"][index]:
                fullDict = {**fullDict, **payload["allOf"][index]["properties"]}
            else:
                fullDict = {**fullDict, **payload["allOf"][index]}
    elif "anyOf" in payload:
        for index in range(len(payload["anyOf"])):
            if "properties" in payload["anyOf"][index]:
                fullDict = {**fullDict, **payload["anyOf"][index]["properties"]}
            else:
                fullDict = {**fullDict, **payload["anyOf"][index]}
    elif "oneOf" in payload:
        for index in range(len(payload["oneOf"])):
            if "properties" in payload["oneOf"][index]:
                fullDict = {**fullDict, **payload["oneOf"][index]["properties"]}
            else:
                fullDict = {**fullDict, **payload["oneOf"][index]}
    else:
        fullDict = payload["properties"].copy()

    # echo("fullDict", fullDict)
    #with open("fullDict.json", "w") as file:
    #    file.write(str(fullDict))

    for prop in fullDict:
        parsedProperty = parse_property({prop: fullDict[prop]}, dataModel, 0)
        # echo("parsedProperty", parsedProperty)
        if prop in ["id"]:
            output = {**output, **parsedProperty}
        elif prop in ["type"]:
            output = {**output, **{prop: parsedProperty}}
        else:
            output = {**output, **{prop: parsedProperty}}
        # echo("output", output)
    output["@context"] = [create_context(subject)]
    # print("======================")
    # print(json.dumps(output))

    return output


# 18
def ngsi_ld_keyvalue_example_generator(schema_url: str):
    """It returns a fake key value ngsi-ld format example based on the given json schema
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json

    Returns:
        if the input parameter exists and the json schema is a valide json:
            a fake key value ngsi-ld format example stored in dictionary format
        if there's any problem related to input parameter and json schema:
            False
    """

    output = ngsi_ld_example_generator(schema_url)
    if not output: return output
    if output == issue_message: return issue_message

    keyvalues = normalized2keyvalues(output)

    return keyvalues

# 19
def geojson_features_example_generator(schema_url: str):
    """It returns a fake geojson feature format example based on the given json schema
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json

    Returns:
        if the input parameter exists and the json schema is a valide json:
            a fake geojson feature format example stored in dictionary format
        if there's any problem related to input parameter and json schema:
            False
    """

    noGeometryMessage = "\"wrong data model for generation of geojson Feature. No geographic properties\""
    output = ngsi_ld_example_generator(schema_url)
    if not output: return output
    if output == issue_message: return issue_message

    basePayload = output
    geopropertyName = ""
    # check that it is possible to generate the geojson feature
    if all(i in basePayload for i in ["id", "type", "location"]):
        geopropertyName = "location"
    else:
        for prop in basePayload:
            if isinstance(basePayload[prop], dict) and ('type' in basePayload[prop]):
                if basePayload[prop]["type"] == "Geoproperty":
                    geopropertyName = prop
        if geopropertyName == "":
            return "{\"error\": " + noGeometryMessage + "}"
    if geopropertyName != "":
        geojsonFeature = {}
        # print(type(basePayload))
        geojsonFeature["id"] = basePayload["id"]
        geojsonFeature["type"] = "Feature"
        geojsonFeature["geometry"] = basePayload[geopropertyName]["value"]
        rawPayload = basePayload.copy()
        rawPayload.pop("id")
        rawPayload.pop("type")
        geojsonFeature["properties"] = rawPayload
        return geojsonFeature
    
# 20
def update_broker(datamodel, subject, attribute, value, entityId=None, serverUrl=None, broker_folder="/ngsi-ld/v1"):
    # inspired by @antonio_jara
    """Update a broker compliant with a specific data model

    Parameters:
        - datamodel: the name of the data model of the SDM (see https://github.com/smart-data-models/data-models/blob/master/specs/AllSubjects/official_list_data_models.json) or this form
        https://smartdatamodels.org/index.php/list-of-data-models-3/
        - subject: the name of the subject, including the prefix dataModel.'subject'
        - attribute: name of the attribute in this data model. The list of available attributes can be found with this form
        https://smartdatamodels.org/index.php/ddbb-of-properties-descriptions/?wdt_column_filter%5B1%5D=WeatherObserved (change WeatherObserved by your data model) or with the function of the pysmartdatamodels sdm.attributes_datamodel(subject, datamodel)
        - value: the value to be updated or inserted
        - entity_id (str): The ID of the entity to update. If left none then the query for the broker is returned
        - serverUrl (str): The URL of the NGSI-LD broker.
        - broker_folder(str): It is supposed that the broker is installed in /ngsi/ld (default) change it if installed other location

    Returns:
        - An array with two values
        - First the boolean result of the operation True if successful and False if not
        - Second a textual context explanation in every case
    """

    # from pysmartdatamodels import pysmartdatamodels as sdm

    def insert_in_broker(broker_url, entity):
        import requests
        import json

        # Convert the entity to JSON-LD format
        json_ld_entity = json.dumps(entity)

        try:
            # Send a POST request to the NSI-LD broker to insert the entity
            response = requests.post(broker_url + broker_folder + "/entities", data=json_ld_entity, headers={"Content-Type": "application/ld+json"})

            # Check the response status code
            if response.status_code == 201:
                return [True, "Successfully inserted in server " + broker_url + " the entity " + str(entity)]
            else:
                print("Failed to insert entity. Status code:", response.status_code)
                return [False, "Failed to insert entity in broker :" + broker_url + " with the status code" + str(response.status_code) + " and this Response:" + response.text + " for this payload " + str(entity)]
        except requests.exceptions.RequestException as e:
            return [False, "An error  type (" + str(e) + ") occurred inserting the entity in broker :" + broker_url ]


    def update_entity_in_broker(entity_id, updated_properties, broker_url):
        """Update an entity in an NGSI-LD broker.

        Parameters:
            - entity_id (str): The ID of the entity to update.
            - updated_properties (dict): A dictionary containing the updated properties of the entity.
            - broker_url (str): The URL of the NGSI-LD broker.

        Returns:
            - bool: True if the update was successful, False otherwise.
        """
        headers = {
            "Content-Type": "application/ld+json",
        }

        entity_url = f"{broker_url}{broker_folder}/entities/{entity_id}/attrs"
        print(entity_url)

        try:
            response = requests.patch(entity_url, json=updated_properties, headers=headers)

            if response.status_code == 204:  # 204 indicates a successful update with no content response
                return True
            else:
                print(f"Failed to update entity. Status code: {response.status_code}.")
                print(response.text)
                return False

        except requests.exceptions.RequestException as e:
            print(f"Failed to update entity: {e}")
            return False

    #load list of DM
    dataModelsListUrl  = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
    dataModelsList = open_jsonref(dataModelsListUrl)["officialList"]
    # for repo in dataModelsList:
    #     print(repo)
    dataModels = [repo["dataModels"] for repo in dataModelsList]
    subjects =  [repo["repoName"] for repo in dataModelsList]
    # print(dataModels)
    # all list of data models (even repeated ones)
    full_list_datamodels  = [element for sublist in dataModels for element in sublist]
    # check if data model exists
    if datamodel not in full_list_datamodels:
        return [False, "Data model: " + datamodel + " not found in any subject"]
    # check if subject exists
    if subject not in subjects:
        return [False, "Subject: " + subject + " not found. Have you include the full dataModel.xxxx name?"]
    # check if data model exists in this subject
    elif subject in subjects:
        found_data_model = False
        if datamodel not in datamodels_subject(subject):
            return [False, "the data model : " + datamodel + " is not found in the subject: " + subject]
        else:
            if attribute not in attributes_datamodel(subject, datamodel):
                return [False, "The attribute : " + attribute + " is not found in the data model: " + datamodel]
            else:
                data_type = datatype_attribute(subject, datamodel, attribute)
                # Define your JSON schema
                schema = {
                    "type": data_type
                }
                try:
                    # Validate the variable against the schema
                    validate(value, schema)
                    print("Variable matches the specified data type.")

                    if entityId is None: # we need to create an entity
                        id_random = "urn:ngsi-ld" + generate_random_string(length=4) + ":" + generate_random_string(length=4)
                        if serverUrl is not None:
                            ngsi_type = ngsi_datatype_attribute(subject, datamodel, attribute)
                            payload = {"id": id_random, "type": datamodel, attribute: {"type": ngsi_type, "value": value}, "@context": create_context(subject)}
                            return insert_in_broker(serverUrl, payload)
                        else: # no entity id and no broker, just returned the payload to be inserted
                            return [True, {"id": id_random, "type": datamodel, attribute: value, "@context": create_context(subject)}]

                    else: # there is an entity so let's update
                        payload = {"id": entityId, "type": datamodel, attribute: value, "@context": create_context(subject)}
                        if serverUrl is not None:
                            result = update_entity_in_broker(entityId, payload, serverUrl)
                            if result:
                                return [result, "succesfully updated this payload" + str(payload)]
                            else:
                                return [result, "There is a problem updating this payload" + str(payload)]
                        else:
                            return[True, "the payload for the update should be this one:" +str(payload)]


                except jsonschema.exceptions.ValidationError as e:
                    print("Variable does not match the specified data type.")
                    print(e)
                    return [False, "The attribute: " + attribute + " cannot store the value : " + str(value)]

# 21
def generate_sql_schema(model_yaml: str) -> str:
    """
    Generate a PostgreSQL schema SQL script from the model.yaml representation of a Smart Data Model.

    Parameters:
        model_yaml (str): url of the model.yaml file (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherAlert/model.yaml)

    Returns:
        str: A string containing the PostgreSQL schema SQL script.
    """

    # open yaml
    model_yaml = open_yaml(model_yaml)

    # Get the entity name
    entity = list(model_yaml.keys())[0]

    # Initialize SQL schema statements
    sql_schema_statements = []
    sql_type_statement = []

    sql_data_types= ""

    # Define format mappings for YAML formats to postgreSQL Schema types
    type_mapping = {
        "string": "TEXT",
        "integer": "INTEGER",
        "number": "NUMERIC",
        "boolean": "BOOLEAN",
        "object": "JSON",
        "array": "JSON",
    }

    # Define format mappings for YAML formats to postgreSQL Schema types
    format_mapping = {
        "date-time": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "uri": "TEXT",
        "email": "TEXT",
        "idn-email": "TEXT",
        "hostname": "TEXT",
        "duration": "TEXT"
    }

    # Start by creating the table
    table_create_statement = f"CREATE TABLE {entity} ("

    for key, value in model_yaml[entity]["properties"].items():
        field_type = "JSON"  # Default to JSON if type is not defined

        # Field type mapping
        if "type" in value:
            if "format" in value:
                # format type mapping (format overrides type)
                field_type = format_mapping.get(value["format"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")
            
            elif "enum" in value:
                enum_values = value["enum"]
                enum_values = [str(element) for element in enum_values]
                if key == "type":
                    field_type = f"{entity}_type"
                else:
                    field_type = f"{key}_type"
                # create sql create type statment
                sql_type_statement.append(f"CREATE TYPE {field_type} AS ENUM ({','.join(map(repr, enum_values))});")

                sql_data_types += "CREATE TYPE " + field_type + " AS ENUM ("
                sql_data_types += f"{','.join(map(repr, enum_values))}"
                sql_data_types += ");"

                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

            else:
                field_type = type_mapping.get(value["type"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"{key} {field_type}")

        # Handle the case when "allOf" exists
        if key == "allOf" and isinstance(value, list):
            for values in value:
                for sub_key, sub_value in values.items():
                    if isinstance(sub_value, dict):
                        if "format" in sub_value:
                            sub_field_type = format_mapping.get(sub_value["format"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
                        if "type" in sub_value:
                            sub_field_type = type_mapping.get(sub_value["type"])
                            sql_schema_statements.append(f"{sub_key} {sub_field_type}")
        if key == "id":
            field_type = "TEXT"

    # Complete the CREATE TABLE statement
    table_create_statement += ", ".join(sql_schema_statements)
    table_create_statement += ");"
    # PostgreSQL schema 
    result = sql_data_types + "\n" + table_create_statement
    print(result)

    return result