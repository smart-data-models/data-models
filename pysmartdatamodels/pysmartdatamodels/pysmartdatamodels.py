import collections
import datetime

import functools
import re

import gzip
import json
import os
import urllib.request

import jsonschema
import pytz
import requests

from jsonschema import validate, Draft202012Validator

import urllib.request

path = __file__

# Find the index of the last occurrence of /
index = path.rfind(os.sep)

# Extract the right part of the string up until the last /
left_part = path[:index]
# lookup install path for - model-assets

from pysmartdatamodels.utils.common_utils import extract_subject_from_raw_url, extract_datamodel_from_raw_url, open_jsonref, parse_property2ngsild_example, normalized2keyvalues_v2, create_context, generate_random_string, is_metadata_properly_reported, is_metadata_existed, schema_output_sum, message_after_check_schema, open_yaml, is_url_existed,  parse_payload_v2, parse_yamlDict

official_list_file_name = left_part + "/model-assets/official_list_data_models.json"
ddbb_attributes_file = left_part + "/model-assets/smartdatamodels.json.gz"
metadata_file = left_part + "/model-assets/datamodels_metadata.json"

# data models that are not able to generate examples from the schema due to certain issue
pending_datamodels = ["SeaportFacilities", "OffStreetParking", "OnStreetParking", "ParkingGroup", "WeatherAlert", "Museum", "MosquitoDensity", "Alert", "MediaEvent",  "DataResourceFrictionlessData", "TableSchemaFrictionlessData", "free_bike_status", "geofencing_zones", "station_information", "station_status", "system_alerts", "Presentation", "DigitalInnovationHub"]
returnPendingMessage = "====== Examples are unable to be generated for the model ====== \nThe current schema may includes open attributes that need further definition, like subproperties inside of object structure, or other inner problems, like infinite recursion and unknown format."

# Regular expression pattern to extract owner, repository, branch, and file path
github_url_pattern = r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)"


@functools.lru_cache(maxsize=1)
def _load_attributes_db():
    """Load and cache the full attributes database (smartdatamodels.json.gz).

    This file has 160,000+ entries and was previously re-read and
    re-parsed from disk on every single call to any of the per-attribute
    lookup functions below (description_attribute, datatype_attribute,
    attributes_datamodel, etc.), each doing its own linear scan. Cached in
    memory for the life of the process -- call update_data() to refresh
    the on-disk file, which also invalidates this cache.
    """
    with gzip.open(ddbb_attributes_file, "rt", encoding='utf-8') as f:
        return json.load(f)


@functools.lru_cache(maxsize=1)
def _load_official_list():
    """Load and cache the official list of data models grouped by subject."""
    with open(official_list_file_name, "r", encoding='utf-8') as f:
        return json.load(f)["officialList"]


@functools.lru_cache(maxsize=1)
def _load_metadata_db():
    """Load and cache the per-data-model metadata file."""
    with open(metadata_file, "r", encoding='utf-8') as f:
        return json.load(f)


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
    output = _load_official_list()
    return output


# 2
def load_all_attributes():
    """Returns an array of objects describing every attribute in the data models
        - _id: identifier of the item
        - property: the name of the attribute
        - dataModel: the data model this attribute is present
        - repoName: the subject this data model belongs to
        - description: the description of the attribute
        - typeNGSI: Whether it is a Property, GeoProperty, or Relationship
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
    output = _load_attributes_db()
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
    datamodelsdict = _load_official_list()
    for item in datamodelsdict:
        output.append(item["repoName"])

    return output


# 5
def datamodels_subject(subject: str):
    """List the names of the data models defined in the subject.
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

    datamodelsdict = _load_official_list()
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
    datamodelsdict = _load_attributes_db()

    # Looks for the attribute in the dictionary
    for item in datamodelsdict:
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
    datamodelsdict = _load_attributes_db()

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
            done = False
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
    datamodelsdict = _load_attributes_db()

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
    datamodelsdict = _load_attributes_db()

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
    datamodelsdict = _load_attributes_db()

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
    """List the NGSI data type of an attribute (Property, Relationship or GeoProperty) belonging to a subject and data model.
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
    datamodelsdict = _load_attributes_db()

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
                  "text": "This will usually be allocated by the storage platform. Entity creation timestamp"
                  },
        - schemaDiagnose: It counts the attributes with right descriptions and those which don't.
        - alreadyUsedProperties: It identifies attributes that have already been used in other data models and includes their definition
        - availableProperties: Identifies those attributes which are not already included in any other data model
    """

    def is_property_already_existed(output: dict, yamlDict: dict) -> dict:
        """Sorts out the properties already existed in the database

        Parameters:
            output (dict): The output dictionary to report properites.
            yamlDict (dict): The yaml dictionary containing information of properties

        Returns:
            dict: The updated output dictionary with property warnings.
        """
        lowKey = None
        existing = "alreadyUsedProperties"
        available = "availableProperties"
        try:
            commonProperties = ["id", "name", "description", "location", "seeAlso", "dateCreated", "dateModified",
                                "source", "alternateName", "dataProvider", "owner", "address", "areaServed", "type"]

            output[existing] = []
            output[available] = []

            # Loaded once outside the loop -- this used to re-open and
            # re-parse the ~5MB gzip attributes database once per
            # non-common property in the schema being validated.
            datamodelsdict = _load_attributes_db()

            for key in yamlDict:
                if key in commonProperties:
                    continue
                lowKey = key.lower()

                results = []
                for item in datamodelsdict:
                    try:
                        if re.match(lowKey, item['property'], re.IGNORECASE):
                            results.append(item)
                    except:
                        nada = 0

                if len(results) > 0:
                    definitions = []
                    dataModelsList = []
                    types = []
                    for index, item in enumerate(results):
                        dataModelsList.append(str(index + 1) + ".-" + item["dataModel"])
                        if "description" in item or "type" in item:
                            if "description" in item:
                                definitions.append(str(index + 1) + ".-" + item["description"])
                            else:
                                definitions.append(str(index + 1) + ".- missing description")
                            if "type" in item:
                                types.append(str(index + 1) + ".-" + item["type"])
                            else:
                                types.append(str(index + 1) + ".- missing type")
                        else:
                            output[existing].append({"Error": lowKey})
                    output[existing].append({key: "Already used in data models: " + ",".join(
                        dataModelsList) + " with these definitions: " + chr(13).join(
                        definitions) + " and these data types: " + ",".join(types)})
                else:
                    output[available].append({key: "Available"})

        except Exception as e:
            output.setdefault(existing, [])
            output[existing].append({"Error": lowKey if lowKey is not None else str(e)})

        return output

    # initialize variables for the script
    output = {}  # the json answering the test
    tz = pytz.timezone("Europe/Madrid")
    metaSchema = open_jsonref("https://json-schema.org/draft/2020-12/meta/validation")
    incompleteDescription = "Incomplete description"
    withoutDescription = "No description at all"

    # validate inputs
    existsSchema = is_url_existed(schema_url)

    # url provided is an existing url
    if not existsSchema[0]:
        output["result"] = False
        output["cause"] = "Cannot find the schema at " + schema_url
        output["time"] = str(datetime.datetime.now(tz=tz))
        print(json.dumps(output))
        return output

    # url is actually a json
    try:
        schemaDict = json.loads(existsSchema[1])
    except ValueError:
        output["result"] = False
        output["cause"] = "Schema " + schema_url + " is not a valid json"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url: ": schema_url}
        print(json.dumps(output))
        return output

    # test that it is a valid schema against the metaschema
    try:
        schema = open_jsonref(schema_url)
        if not bool(schema):
            output["result"] = False
            output["cause"] = "json schema returned empty (wrong $ref?)"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schema_url: ": schema_url}
            print(json.dumps(output))
            return output

    except:
        output["result"] = False
        output["cause"] = "json schema cannot be fully loaded"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        return output

    try:
        validate(instance=schema, schema=metaSchema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    except jsonschema.exceptions.ValidationError as err:
        # print(err)
        output["result"] = False
        output["cause"] = "schema does not validate as a json schema"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        output["errorSchema"] = str(err)
        print(json.dumps(output))
        return output

    # extract properties' definitions
    # check if they are populated
    documented = "documentationStatusOfProperties"
    try:
        yamlDict, attributes = parse_payload_v2(schema, 1)
    except:
        output["result"] = False
        output["cause"] = "schema cannot be loaded (possibly invalid $ref)"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        return output

    # check the duplicated attributes
    if len(attributes[2]) != len(set(attributes[2])):

        def find_duplicates(input_list: list) -> list:
            """
            Find and output the duplicated values inside a list.
            Parameters:
                input_list (list): The list to search for duplicates in.
            Returns:
                list: A list containing the duplicated values found in the input list.
            """
            seen = set()
            duplicates = set()

            for item in input_list:
                if item in seen:
                    duplicates.add(item)
                else:
                    seen.add(item)

            return list(duplicates)

        output["result"] = False
        output[
            "cause"] = f"Duplicated attributes (User-defined properties is duplicated with system-defined properties):\n\t{', '.join(find_duplicates(attributes[2]))}"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        return output

    output[documented] = parse_yamlDict(yamlDict, schema_url, 1)
    allProperties = 0
    documentedProperties = 0
    faultyDescriptionProperties = 0
    notDescribedProperties = 0
    for key in output[documented]:
        allProperties += 1
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
    # TODO
    output = is_property_already_existed(output, yamlDict)

    # now it checks if the metadata is properly reported
    output = is_metadata_properly_reported(output, schemaDict)

    # now it checks if the metadata does exist
    output = is_metadata_existed(output, schemaDict, schema_url, message="schema")

    # make a summary of all the output
    results = schema_output_sum(output)

    # print out the collective message after the schema check
    print(message_after_check_schema(results))

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
    datamodelsdict = _load_attributes_db()

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
    selectedattributes = []
    for d in datamodelsdict:
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
            try:
                # if all metadata are available for the attribute it is done in one shot
                selectedmeta = [item[d] for d in listedmetadata]
                row = separator.join(selectedmeta)
            except KeyError:
                # if all metadata are not available for the attribute it is done with a loop
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


# 14
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

    datamodelsdict = _load_official_list()
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

    datamodelsdict = _load_official_list()
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

    # Download the latest data files from a remote server.
    # smartdatamodels.json.gz is fetched pre-compressed from the server --
    # ~5MB instead of the ~110MB uncompressed file -- since that's the format
    # this module reads it in anyway (see ddbb_attributes_file above).
    urllib.request.urlretrieve("https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json", os.path.join(data_dir, "official_list_data_models.json"))
    urllib.request.urlretrieve("https://smartdatamodels.org/extra/smartdatamodels.json.gz", os.path.join(data_dir, "smartdatamodels.json.gz"))
    urllib.request.urlretrieve("https://smartdatamodels.org/extra/datamodels_metadata.json", os.path.join(data_dir, "datamodels_metadata.json"))

    # The three files above are cached in memory (see _load_attributes_db,
    # _load_official_list, _load_metadata_db) -- without clearing those
    # caches here, a long-running process that calls update_data() would
    # keep serving the pre-update data for the rest of its lifetime.
    _load_attributes_db.cache_clear()
    _load_official_list.cache_clear()
    _load_metadata_db.cache_clear()


# 17
def ngsi_ld_example_generator(schema_url: str):
    """It returns a fake normalized ngsi-ld format example based on the given json schema
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json

    Returns:
        if the input parameter exists and the json schema is a valid json:
            a fake normalized ngsi-ld format example stored in dictionary format
        if there's any problem related to input parameter and json schema:
            False
    """

    dataModel = extract_datamodel_from_raw_url(schema_url)
    subject = extract_subject_from_raw_url(schema_url)

    # Both dataModel and subject need to be successfully extracted
    # dataModel is not in the list of pending that are unable to generate
    if dataModel == "dataModel" or subject == "subject": return False
    if dataModel in pending_datamodels: return returnPendingMessage

    payload = open_jsonref(schema_url)
    if payload == "": return False

    output = {}
    fullDict = {}

    # Parse the "allOf", "anyOf", "oneOf" structure
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

    for prop in fullDict:

        parsedProperty = parse_property2ngsild_example({prop: fullDict[prop]}, dataModel, 0)

        # id and type should be key-value format in ngsild format
        if prop in ["id"]:
            output = {**output, **parsedProperty}
        elif prop in ["type"]:
            output = {**output, **{prop: parsedProperty}}
        else:
            output = {**output, **{prop: parsedProperty}}

    output["@context"] = [create_context(subject)]

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
    if output == returnPendingMessage: return returnPendingMessage

    # normalized2keyvalues is deprecated
    keyvalues = normalized2keyvalues_v2(output)

    return keyvalues


#19
def geojson_features_example_generator(schema_url: str):
    # TODO: Add ranges to the generated values of the different attributes
    """It returns a fake geojson feature format example based on the given json schema
    Parameters:
        schema_url: url of the schema (public available). (i.e. raw version of a GitHub repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json

    Returns:
        if the input parameter exists and the json schema is a valide json:
            a fake geojson feature format example stored in dictionary format
        if there's any problem related to input parameter and json schema:
            False
    """

    noGeometryMessage = "\"wrong data model for generation of geojson Feature. No geographic properties\""
    output = ngsi_ld_example_generator(schema_url)
    if not output: return output
    if output == returnPendingMessage: return returnPendingMessage

    basePayload = output
    geopropertyName = ""
    # check that it is possible to generate the geojson feature
    if all(i in basePayload for i in ["id", "type", "location"]):
        geopropertyName = "location"
    else:
        for prop in basePayload:
            if isinstance(basePayload[prop], dict) and ('type' in basePayload[prop]):
                if basePayload[prop]["type"] == "GeoProperty":
                    geopropertyName = prop
        if geopropertyName == "":
            return "{\"error\": " + noGeometryMessage + "}"
    if geopropertyName != "":
        geojsonFeature = {}
        geojsonFeature["id"] = basePayload["id"]
        geojsonFeature["type"] = "Feature"
        geojsonFeature["geometry"] = basePayload[geopropertyName]["value"]
        rawPayload = basePayload.copy()
        rawPayload.pop("id")
        rawPayload.pop("type")
        geojsonFeature["properties"] = rawPayload
        return geojsonFeature


#20
def update_broker(datamodel, subject, attribute, value, entityId=None, serverUrl=None, broker_folder="/ngsi-ld/v1", updateThenCreate=True):
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
        - updateThenCreate: If the updating attribute is nonexistent in the wanting entity, then create the attribute first if updateThenCreate is True, otherwise the operation is illegal

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
            response = requests.post(broker_url + broker_folder + "/entities", data=json_ld_entity,
                                     headers={"Content-Type": "application/ld+json"})

            # Check the response status code
            if response.status_code == 201:
                return [True, "Successfully inserted in server " + broker_url + " the entity " + str(entity)]
            else:
                print("Failed to insert entity. Status code:", response.status_code)
                return [False, "Failed to insert entity in broker :" + broker_url + " with the status code" + str(
                    response.status_code) + " and this Response:" + response.text + " for this payload " + str(entity)]
        except requests.exceptions.RequestException as e:
            return [False, "An error  type (" + str(e) + ") occurred inserting the entity in broker :" + broker_url]

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
            elif response.status_code == 207:
                if updateThenCreate:
                    ngsi_type = ngsi_datatype_attribute(subject, datamodel, attribute)
                    create_properties = {attribute: {"type": ngsi_type, "value": value}}
                    create_headers = {
                        'Content-Type': 'application/json',
                        'Link': f'<{create_context(subject)}>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
                    }

                    try:
                        create_response = requests.post(entity_url, json=create_properties, headers=create_headers)
                        if create_response.status_code == 204:  # 204 indicates a successful update with no content response
                            return True
                        else:
                            print(
                                f"Failed to update entity with nonexistent attribute. Status code: {create_response.status_code}.")
                            print(create_response.text)
                            return False

                    except requests.exceptions.RequestException as e:
                        print(f"Failed to update entity with nonexistent attribute: {e}")
                        return False
                else:
                    print(
                        f"Failed to update entity. Trying to update nonexistent attributes. If so, set updateThenCreate to true.")
                    return False
            else:
                print(f"Failed to update entity. Status code: {response.status_code}.")
                print(response.text)
                return False

        except requests.exceptions.RequestException as e:
            print(f"Failed to update entity: {e}")
            return False

    # load list of DM
    dataModelsListUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
    dataModelsList = open_jsonref(dataModelsListUrl)["officialList"]
    # for repo in dataModelsList:
    #     print(repo)
    dataModels = [repo["dataModels"] for repo in dataModelsList]
    subjects = [repo["repoName"] for repo in dataModelsList]
    # print(dataModels)
    # all list of data models (even repeated ones)
    full_list_datamodels = [element for sublist in dataModels for element in sublist]
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

                    if entityId is None:  # we need to create an entity
                        id_random = "urn:ngsi-ld" + generate_random_string(length=4) + ":" + generate_random_string(
                            length=4)
                        if serverUrl is not None:
                            ngsi_type = ngsi_datatype_attribute(subject, datamodel, attribute)
                            if ngsi_type == "Relationship":
                                payload = {"id": id_random, "type": datamodel,
                                           attribute: {"type": ngsi_type, "object": value},
                                           "@context": create_context(subject)}
                            else:
                                payload = {"id": id_random, "type": datamodel,
                                           attribute: {"type": ngsi_type, "value": value},
                                           "@context": create_context(subject)}
                            return insert_in_broker(serverUrl, payload)
                        else:  # no entity id and no broker, just returned the payload to be inserted
                            return [True, {"id": id_random, "type": datamodel, attribute: value,
                                           "@context": create_context(subject)}]

                    else:  # there is an entity so let's update
                        payload = {"id": entityId, "type": datamodel, attribute: value,
                                   "@context": create_context(subject)}
                        if serverUrl is not None:
                            result = update_entity_in_broker(entityId, payload, serverUrl)
                            if result:
                                return [result, "succesfully updated this payload" + str(payload)]
                            else:
                                return [result, "There is a problem updating this payload" + str(payload)]
                        else:
                            return [True, "the payload for the update should be this one:" + str(payload)]


                except jsonschema.exceptions.ValidationError as e:
                    print("Variable does not match the specified data type.")
                    print(e)
                    return [False, "The attribute: " + attribute + " cannot store the value : " + str(value)]


#21
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

    sql_data_types = ""

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
        # "id" always maps to the primary key column, regardless of what
        # "type"/"format"/etc. it declares -- handle it here and move on, so
        # it isn't *also* appended by the type-mapping branches below (that
        # produced a duplicate "id" column in every generated schema, since
        # id properties almost always declare a "type").
        if key == "id":
            field_type = "TEXT PRIMARY KEY"
            sql_schema_statements.append(f"\"{key}\" {field_type}")
            continue

        field_type = "JSON"  # Default to JSON if type is not defined

        # Field type mapping
        if "type" in value:
            if "format" in value:
                # format type mapping (format overrides type)
                field_type = format_mapping.get(value["format"])
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"\"{key}\" {field_type}")

            elif "enum" in value:
                enum_values = value["enum"]
                enum_values = [str(element) for element in enum_values]
                # Namespaced per entity (not just f"{key}_type") so two
                # unrelated models that happen to both have e.g. a "status"
                # enum don't generate an identically-named CREATE TYPE,
                # which made it impossible to load more than one model's
                # schema.sql into the same database -- see
                # smart-data-models/data-models#74.
                if key == "type":
                    field_type = f"{entity}_type"
                else:
                    field_type = f"{entity}_{key}_type"
                sql_data_types += "CREATE TYPE " + field_type + " AS ENUM ("
                sql_data_types += f"{','.join(map(repr, enum_values))}"
                sql_data_types += ");"

                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"\"{key}\" {field_type}")

            else:
                # A multityped attribute (e.g. type: [Property, Relationship])
                # loads as a list, which isn't hashable -- dict.get() would
                # raise TypeError instead of falling through to the
                # documented "JSON" default for cases this exporter doesn't
                # fully translate. An unrecognized-but-hashable type (e.g. a
                # typo) previously fell through to field_type = None,
                # silently producing invalid SQL ("key" None) -- also
                # defaulted to JSON now.
                raw_type = value["type"]
                field_type = type_mapping.get(raw_type, "JSON") if isinstance(raw_type, str) else "JSON"
                # add attribute to the SQL schema statement
                sql_schema_statements.append(f"\"{key}\" {field_type}")
        elif "oneOf" in value or "anyOf" in value:
            field_type = "JSON"
            sql_schema_statements.append(f"\"{key}\" {field_type}")

        # Handle the case when a property is itself composed via "allOf"
        # (e.g. properties.<name>.allOf: [...]) -- note this is the property's
        # *value* containing "allOf", not a property literally named "allOf".
        elif "allOf" in value and isinstance(value["allOf"], list):
            for values in value["allOf"]:
                for sub_key, sub_value in values.items():
                    if isinstance(sub_value, dict):
                        if "format" in sub_value:
                            sub_field_type = format_mapping.get(sub_value["format"])
                            sql_schema_statements.append(f"\"{sub_key}\" {sub_field_type}")
                        if "type" in sub_value:
                            sub_field_type = type_mapping.get(sub_value["type"])
                            sql_schema_statements.append(f"\"{sub_key}\" {sub_field_type}")

    # Complete the CREATE TABLE statement
    table_create_statement += ", ".join(sql_schema_statements)
    table_create_statement += ");"
    # PostgreSQL schema
    result = sql_data_types + "\n" + table_create_statement

    return result


# 22
def look_for_datamodel(datamodel_search_text, approx_percentage = 0):

    """Look for the data models that match the text included

    Parameters:
        - datamodel_search_text: piece of string with a text to be searched across the name of the data model of the SDM (It can be a part of the data model name)
        - approx_percentage: optional parameter, in case a non-exact matching is required, percentage of likelikhood between 0 and 99. i.e. 90 means quite similar. Example Weather is 64% similar to WeatherObserved, or 74% to WeatherAlert

    Returns:
        - An array with the values of the matching data models names

    """
    from fuzzywuzzy import fuzz
    # library to enable the fuzzy search

    datamodels = list_all_datamodels()
    output = []
    if approx_percentage == 0:
        output = [dm for dm in datamodels if datamodel_search_text in dm]
    else:
        output = [dm  for dm in datamodels if (fuzz.ratio(dm, datamodel_search_text) > approx_percentage)]
    return output


# 23
def list_datamodel_metadata(datamodel, subject):
    """Look for the metadata data models that match the text included

       Parameters:
           - datamodel: Exact name of the data model
           - subject: Exact name of the subject

       Returns:
           - An object  with the metadata available for this data model in the different subjects
                -   version
                i.e. "0.0.2"
                -   modelTags
                i.e. "GreenMov"
                -   title of the data model
                i.e. "Smart Data Models. User Context schema"
                -   $id single link to the schema"
                i.e. https://smart-data-models.github.io/dataModel.User/UserContext/schema.json"
                -   description del data model
                i.e. "Information on the context of an anonymized in a given point in time"
                -   required attributes (array)
                i.e. ["id", "type"]
                -   yamlUrl link to the yaml version of the schema (model.yaml)
                i.e. https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/model.yaml
                -   jsonSchemaUrl link to the schema (schema.json)
                i.e. https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/schema.json"
                -   @context location of the @context of the subject.
                i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/context.jsonld"
                - exampleKeyvaluesJson link to the example in key values for NGSI v2 (json)
                i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example.json"
                 - exampleKeyvaluesJsonld link to the example in key values for NGSI LD (jsonld)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example.jsonld"
                 - exampleNormalizedJson link to the example in normalized for NGSI v2 (json)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example-normalized.json"
                 - exampleNormalizedJsonld link to the example in normalized for NGSI LD (jsonld)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example-normalized.jsonld"
                 - sql sql export of the schema.
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/schema.sql"
                 - adopters	list of the adopters of the data model
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/ADOPTERS.yaml"
                 - contributors	list of the contributors of the subject
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/CONTRIBUTORS.yaml"
                 - spec Specification in English
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec.md"
                 - spec_DE Specification in German
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_DE.md"
                 - spec_ES Specification in Spanish
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_ES.md"
                 - spec_FR Specification in French
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_FR.md"
                 - spec_IT Specification in Italian
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_IT.md"
                 - spec_JA Specification in Japanese
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_JA.md"
                 - spec_KO Specification in Korean
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_KO.md"
                 - spec_ZH Specification in Chinese
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/doc/spec_ZH.md"
           - if the data model is not found it returs False
           """

    output = []

    # Opens the file with the metadata about the data models
    metadata_dict = _load_metadata_db()

    # It looks if this datamodel-subject pair is in the metadata. Although only one result is expected execution this way is quicker than other alternatives
    output = [metadata for metadata in metadata_dict if (metadata["dataModel"] == datamodel) and (metadata["subject"] == subject)]

    # returns the outcome
    if len(output) == 0:
        return False
    else:
        return output[0]



    # def validate_payload(datamodel, subject, payload):
    # TODO: Add this function to the package in next version
    """Validates a payload against a data model 

       Parameters:
           - datamodel: Exact name of the data model
           - subject: Exact name of the subject
           - payload: key values format of payload to be validated

       Returns:
           - An object with two subattributes 
                -   result: True or false
                -   details: Details about the successful validation 
                -   Case True: I.e. if there is a warning like exceeding attributes present but not in the data model)
                -   Case False: I.e. the outcome of the validation library

        Remarks for the development
        -   Maybe the libraries jsonschema, json-checker, pydantic could be useful here
        - Structure: 
        -   validate the inputs
        -       validate that the payload is a real and valid json
        -       validate that there is a type attribute coinciding to the data model name
        -       validate that the pointed data model really exist in the database 
    """

    # def create_QR_code(datamodel, subject):
    # TODO: Add this function to the package in next version
    """Look for the metadata data models that match the text included

       Parameters:
           - datamodel: Exact name of the data model
           - subject: Exact name of the subject

       Returns:
           - An image payload  
                

        Remarks for the development
        -   This code below creates such QR 
        - It has to 
        -   1) be adapted to the input parameters and to the output format
        - Remove own functions already present in the package
        -   2) include the new required packages in the requirements of the package
        - Maybe this internal procedure for extending the package can help on getting all the details https://smartdatamodels.org/index.php/procedure-to-extend-pysmartdatamodels-package/ of course not all tasks need to be accomplished if you are extending the package in your PR  
        
        def create_qr_image(filename, repo_name, dataModel):
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    from github import Github

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
            # test

    logo_path = "smartdatamodels.png"
    credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
    # credentialsFile = "/home/fiware/credentials.json"
    credentials = open_json(credentialsFile)
    access_token = credentials["token"]
    repo_owner = credentials["globalUser"]
    g = Github(access_token)
    repo = g.get_organization(repo_owner).get_repo(repo_name)


    # Generate QR code image
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    url = f"https://github.com/{repo_owner}/{repo_name}/blob/master/{dataModel}/doc/spec.md"

    qr.add_data(url)
    qr.make(fit=True)
    # img = qr.make_image(fill_color="#002e67", back_color="white")
    img = qr.make_image(fill_color="#002e67", back_color="white")
    border_size = 24
    border = Image.new("RGB", (img.size[0] + border_size * 2, img.size[1] + border_size * 2), "white")
    border.paste(img, (border_size, border_size))

    # Add the letter
    draw = ImageDraw.Draw(border)
    font = ImageFont.truetype("arial.ttf", 20)
    draw.text((border_size, border_size), "Structure of the Data model:" + dataModel, font=font, fill="#002e67")
    moreinfo  = "FIWARE Foundation. info@smartdatamodels.org"
    draw.text((border_size, border_size + img.size[0]), moreinfo, fill="#002e67", font=font,)
    # Add the logo
    logo = Image.open(logo_path)
    logo_size = int(border_size * 2.5)
    logo = logo.resize((logo_size, logo_size))
    border.paste(logo, (
    int((border_size * 2 + img.size[0] - logo_size) / 2), int((border_size * 2 + img.size[1] - logo_size) / 2)))

    # Save image to file
    border.save(filename)

    # Upload file to GitHub repository
    with open(filename, "rb") as f:
        content = f.read()
    # repo.create_file(dataModel + "/" + filename, "QR image", content)
 
    """

    # def include_local_datamodel(schema, subject, datamodel, contributors (optional), adopters (optional), notes(optional)):
    # TODO: Add this function to the package in next version
    """The aim of this function is to allow the users to include new data models locally 
    This information will not be shared with the central repository unless the user is really willing to do it with an additional functions (see submit datamodel function)

       Parameters:
           - schema: In json schema with the description meeting the contribution manual https://bit.ly/contribution_manual
           - subject: Exact name of the proposed local subject
           - datamodel: name of the proposed data model 
           - contributors: Optional parameter. List of the contributors of the data model (usually it is a pointer to an external file in yaml like this one https://github.com/smart-data-models/dataModel.Transportation/blob/master/CONTRIBUTORS.yaml
           - adopters: Optional parameter. List of the adopters of the data model (usually it is a pointer to an external file in yaml like this one https://github.com/smart-data-models/dataModel.Transportation/blob/master/APDSObservation/ADOPTERS.yaml
           
       Returns:
           - Extends the files located ad model-assets/smartdatamodels.json.gz, official_list_data_models and datamodels_metadata.json.
           - As a result local data models will be treated absolutely like the official ones
                   
        Remarks for the development
        -   The new subject-datamodel pair should be different from an existing one to prevent overwriting existing data models
        - Maybe it could be useful for the development the current script we have for running the inventory of the database https://github.com/smart-data-models/data-models/blob/master/utils/30_f_properties_inventory_10.0.py
          
    """

    # def submit_datamodel(subject, datamodel, contributors (optional), adopters (optional), notes(optional), example_payload, notes_context, public_repository, credentials):
    # TODO: Add this function to the package in next version
    """The aim of this function is to allow the users to share their local data models to the central repository in order to get it accepted
    The function will create the structure expected in the local repository provided, eventually this local repository could be the incubated.  
    
       Parameters:
           - subject: Exact name of the proposed local subject
           - datamodel: name of the proposed data model 
           - contributors: Optional parameter. List of the contributors of the data model (usually it is a pointer to an external file in yaml like this one https://github.com/smart-data-models/dataModel.Transportation/blob/master/CONTRIBUTORS.yaml
           - adopters: Optional parameter. List of the adopters of the data model (usually it is a pointer to an external file in yaml like this one https://github.com/smart-data-models/dataModel.Transportation/blob/master/APDSObservation/ADOPTERS.yaml

       Returns:
           - A PR in the selected repository creating according to the structure described in the contribution manual https://docs.google.com/presentation/d/e/2PACX-1vTs-Ng5dIAwkg91oTTUdt8ua7woBXhPnwavZ0FxgR8BsAI_Ek3C5q97Nd94HS8KhP-r_quD4H0fgyt3/pub?start=false&loop=false&delayms=3000#slide=id.g280c21c8f96_0_124 (page 10 contribution manual)
           - Eventually a mail to info@smartdatamodels.org announcing the availability of the repo in order to start the accepting process.

        

    """


# 24
def validate_dcat_ap_distribution_sdm(json_data):
    """The function takes a distribution DCAT-AP in json and validates if the downloadURL contains a valid payload against conformsTo.
    It works when the downloadURL contains a json keyvalues payload and
    conformsTo point to the raw version of a Smart Data Model
       Parameters:
           json_data: metadata in DCAT-AP distribution format (See https://github.com/smart-data-models/dataModel.DCAT-AP/blob/master/Distribution/schema.json and
           https://semiceu.github.io/DCAT-AP/releases/3.0.0/
                conformsTo: Attribute (Array) with links to the json schemas of SDM
                downloadURL: Public available link to the raw format of the payload

       Returns:
           It prints a version of the attributes separated by the separator listing the meta_attributes specified
           A variable with the same strings
           if any of the input parameters is not found it returns False
    """

    validated = False
    try:
        conforms_to = json_data.get('conformsTo', [])  # retrieves the attribute conformsTo
    except:
        return False

    ################## SECTION FOR VALIDATION WITH SMART DATA MODELS ##################
    valid_link = any(link.startswith('https://github.com/smart-data-models') or link.startswith(
        "https://raw.githubusercontent.com/smart-data-models") for link in conforms_to)
    # it checks that the link belong to smart data Models
    # it should point to the raw version of the json schema
    if not valid_link:
        print(
            'Warning: "conformsTo" attribute should contain at least one link belonging to the domain github.com/smart-data-models')
        return validated
    schemas = [link for link in conforms_to if
               link.startswith('https://github.com/smart-data-models') or link.startswith(
                   "https://raw.githubusercontent.com/smart-data-models")]
    # only those schemas belonging to Smart Data Models are analysed

    # Check if 'downloadURL' attribute points to a valid location to download a file
    if json_data.get('downloadURL', '') is None:
        print('Warning: "I cannot access the distribution URL')
        return validated
    else:
        download_url = json_data.get('downloadURL')

    for distribution in download_url:
        payload = open_jsonref(distribution)  # It retrieves the content of the payload to be validated
        for schema in schemas:
            schema = open_jsonref(schema)  # It retrieves the schema for validating the payload
            try:
                validate(instance=payload, schema=schema)
                print("The download URL content is validated by the JSON schema.")
                # If you reach this point, the content is validated by the current schema
                validated = True
                break
            except Exception as e:
                # If the content is not validated by the current schema, try the next one
                continue
        else:
            print("The download URL content is not validated by any of the JSON schemas.")
            return validated

    return validated
    ################## END OF SECTION FOR VALIDATION WITH SMART DATA MODELS ##################


# 25
def subject_for_datamodel(datamodel):
    """The function looks for the subject corresponding to a data model name
    if not found it returns false
       Parameters:
           datamodel: name of the data model

       Returns:
           An array (always) if there is only one element with the names of the subjects
           Usually only one element in the array is returned because there are few clashes in data model names
           False if no subject is found
    """

    list_of_datamodels = _load_official_list()
    subjects = [repo["repoName"] for repo in list_of_datamodels if datamodel in repo["dataModels"]]
    if len(subjects) == 0:
        return False
    else:
        return subjects


#26
def validate_payload(datamodel, subject, payload):
    """Look for the metadata data models that match the text included

       Parameters:
           - datamodel: Exact name of the data model
           - subject: Exact name of the subject
           - payload: key values format of payload to be validated

       Returns:
           - An object with two subattributes
                -   result: True or false
                -   details: Details about the succesful validation
                -   Case True: I.e. if there is a warning like exceeding attributes present but not in the data model)
                -   Case False: I.e. the outcome of the validation library

        Remarks for the development
        -   Maybe the libraries jsonschema, json-checker, pydantic could be useful here
        - Structure:
        -   validate the inputs
        -       validate that the payload is a real and valid json
        -       validate that there is a type attribute coinciding to the data model name
        -       validate that the pointed data model really exist in the database
    """
    details = []

    # validate that the payload is a real json object (key-values format,
    # not a normalized-NGSI payload with {"type": "Property", "value": ...}
    # envelopes -- this validates against the plain schema.json)
    if not isinstance(payload, dict):
        return {"result": False, "details": [f"payload must be a JSON object (dict), got {type(payload).__name__}"]}

    # validate that the pointed data model really exists in that subject
    datamodels_in_subject = datamodels_subject(subject)
    if datamodels_in_subject is False:
        return {"result": False, "details": [f"Subject '{subject}' not found"]}
    if datamodel not in datamodels_in_subject:
        return {"result": False, "details": [f"Data model '{datamodel}' not found in subject '{subject}'"]}

    # validate that there is a type attribute coinciding with the data model name
    if payload.get("type") != datamodel:
        return {
            "result": False,
            "details": [
                f"payload's \"type\" ({payload.get('type')!r}) does not match the data model name ({datamodel!r})"
            ],
        }

    # fetch and resolve the actual schema, then validate the payload against it
    schema_url = f"https://raw.githubusercontent.com/smart-data-models/{subject}/master/{datamodel}/schema.json"
    try:
        schema = open_jsonref(schema_url)
    except Exception as e:
        return {"result": False, "details": [f"Cannot fetch/parse schema at {schema_url}: {e}"]}
    if not schema:
        return {"result": False, "details": [f"Cannot fetch/parse schema at {schema_url}"]}

    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if schema_errors:
        for err in schema_errors:
            path = ".".join(str(p) for p in err.path) or "(root)"
            details.append(f"{path}: {err.message}")
        return {"result": False, "details": details}

    # the payload is schema-valid -- separately flag (as a warning, not a
    # failure) any top-level attribute not defined in the data model, since
    # jsonschema only rejects this when additionalProperties: false is set,
    # which Smart Data Models schemas generally don't set
    try:
        known_properties, _ = parse_payload_v2(schema, 1)
        unknown = [k for k in payload if k not in known_properties and k != "@context"]
        if unknown:
            details.append(f"Warning: attribute(s) not defined in the data model: {', '.join(unknown)}")
    except Exception:
        pass

    return {"result": True, "details": details or ["payload is valid"]}


# -- identify_or_draft_datamodel and its helpers -----------------------------

_COMMON_SCHEMA_URL = "https://smart-data-models.github.io/data-models/common-schema.json"
_GSMA_COMMONS_PROPERTIES = {
    "id", "dateCreated", "dateModified", "source", "name", "alternateName",
    "description", "dataProvider", "owner", "seeAlso",
}
_LOCATION_COMMONS_PROPERTIES = {"location", "address", "areaServed"}


@functools.lru_cache(maxsize=1)
def _build_attribute_index():
    """Group the cached attributes database by (subject, dataModel) -> set of
    its property names. Built once (then cached) from the same in-memory
    data _load_attributes_db() already holds, for fuzzy-matching an unknown
    payload's attribute names against every known data model at once instead
    of looking them up one at a time.
    """
    index = {}
    for item in _load_attributes_db():
        subject = item.get("repoName")
        datamodel = item.get("dataModel")
        prop = item.get("property")
        if subject is None or datamodel is None or prop is None:
            continue
        index.setdefault((subject, datamodel), set()).add(prop)
    return index


_COMMON_ATTRIBUTE_NAMES = _GSMA_COMMONS_PROPERTIES | _LOCATION_COMMONS_PROPERTIES | {"id", "type"}


def _fuzzy_match_candidates(payload_keys, top_n=5):
    """Rank known data models by what fraction of the payload's own
    (non-common) attribute names also appear in each model's attribute set.

    This is "payload coverage", not Jaccard similarity: the denominator is
    the payload's own attribute count, not the union with the model's full
    attribute set. Jaccard systematically penalizes a real, correct match
    whenever the payload doesn't populate every optional attribute the
    model defines -- which is the normal case, not the exception, so a
    genuinely correct match could score as low as ~0.3 even with zero
    wrong attributes. Coverage reports what it actually should: "of what
    you gave me, how much of it belongs to this model."

    GSMA-Commons/Location-Commons attributes (name, description, location,
    ...) and id/type are excluded from both sides, since nearly every
    model has them -- without this, a payload using only those common
    attributes would score 100% against almost the entire catalog, which
    was verified to happen (1,035 of ~1,118 models) before this exclusion
    was added.

    Returns a list of {"subject", "dataModel", "score"} dicts, highest
    score first. Still a noisy signal, not an identification -- a high
    score means "most of what you gave me belongs to this model," not
    "this payload is complete or correct for this model."
    """
    keys = set(payload_keys) - _COMMON_ATTRIBUTE_NAMES
    if not keys:
        return []
    scored = []
    for (subject, datamodel), attrs in _build_attribute_index().items():
        attrs = attrs - _COMMON_ATTRIBUTE_NAMES
        if not attrs:
            continue
        score = len(keys & attrs) / len(keys)
        if score > 0:
            scored.append({"subject": subject, "dataModel": datamodel, "score": round(score, 3)})
    scored.sort(key=lambda c: c["score"], reverse=True)
    return scored[:top_n]


def _looks_like_geojson(value):
    return (
        isinstance(value, dict)
        and value.get("type") in ("Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon")
        and "coordinates" in value
    )


def _infer_ngsi_type(key, value):
    """Heuristic NGSI type guess for a draft schema -- GeoProperty for
    GeoJSON-shaped values, Relationship for the refXxx naming convention
    (e.g. refDevice), Property for everything else. This is a guess to
    label the TODO placeholder, not a validated classification."""
    if _looks_like_geojson(value):
        return "GeoProperty"
    if len(key) > 3 and key.startswith("ref") and key[3].isupper():
        return "Relationship"
    return "Property"


@functools.lru_cache(maxsize=1)
def _build_property_name_index():
    """Group the cached attributes database by property name -> list of
    every entry using that exact name across every model (regardless of
    which data model or subject it belongs to). Used to reuse an existing
    attribute's description/model/units when drafting a new schema instead
    of emitting a bare TODO for a name that's already well-established
    elsewhere in the catalog (e.g. "precipitation", "solarRadiation")."""
    index = {}
    for item in _load_attributes_db():
        prop = item.get("property")
        if prop is None:
            continue
        index.setdefault(prop, []).append(item)
    return index


def _lookup_known_attribute(property_name):
    """Returns the most common existing definition of this exact property
    name elsewhere in the catalog -- {"description", "model", "units",
    "typeNGSI", "occurrences"} -- or None if the name has never appeared.

    Many attribute names are reused verbatim with a consistent description
    across models (precipitation, solarRadiation, ...); some common/generic
    names (temperature, status, ...) are used with genuinely different
    descriptions by unrelated models. Picking the most common description
    for the name is a reasonable default either way: for the consistent
    case it's exactly right, for the generic case it's still a real,
    plausible starting point for a human to edit -- strictly more useful
    than a bare TODO, even though it isn't guaranteed to fit this draft.
    """
    matches = _build_property_name_index().get(property_name)
    if not matches:
        return None
    descriptions = collections.Counter(m.get("description") for m in matches if m.get("description"))
    if not descriptions:
        return None
    best_description = descriptions.most_common(1)[0][0]
    for m in matches:
        if m.get("description") == best_description:
            return {
                "description": best_description,
                "model": m.get("model"),
                "units": m.get("units"),
                "typeNGSI": m.get("typeNGSI"),
                "occurrences": len(matches),
            }
    return None


def _format_description(ngsi_type, description=None, model=None, units=None):
    """Assemble a description string matching the real convention used
    throughout Smart Data Models schemas, e.g.
    "Property. Model:'https://schema.org/Number'. Amount of water rain. Units:'Liters per square meter'"."""
    text = f"{ngsi_type}."
    if model:
        text += f" Model:'{model}'."
    text += f" {description}" if description else " TODO: describe this attribute."
    if units:
        if not text.endswith("."):
            text += "."
        text += f" Units:'{units}'"
    return text


def _infer_property_schema(key, value):
    """Build one property's draft JSON Schema fragment from a sample value.
    If this exact attribute name is already used elsewhere in the catalog,
    its existing description/model/units are reused instead of a bare
    TODO -- see _lookup_known_attribute. Otherwise the description is an
    explicit TODO, since a sample value tells you a shape, never a
    meaning, and this never fabricates a plausible-looking description."""
    known = _lookup_known_attribute(key)
    ngsi_type = (known and known.get("typeNGSI")) or _infer_ngsi_type(key, value)
    if known:
        description = _format_description(ngsi_type, known.get("description"), known.get("model"), known.get("units"))
    else:
        description = _format_description(ngsi_type)

    if isinstance(value, bool):
        return {"type": "boolean", "description": description}
    if isinstance(value, int):
        return {"type": "integer", "description": description}
    if isinstance(value, float):
        return {"type": "number", "description": description}
    if isinstance(value, str):
        return {"type": "string", "description": description}
    if isinstance(value, list):
        schema = {"type": "array", "description": description}
        if value:
            schema["items"] = _infer_property_schema(key, value[0])
            schema["items"].pop("description", None)
        return schema
    if isinstance(value, dict):
        if _looks_like_geojson(value):
            return {
                "type": "object",
                "description": description,
                "properties": {
                    "type": {"type": "string", "enum": [value["type"]]},
                    "coordinates": {"type": "array"},
                },
            }
        return {
            "type": "object",
            "description": description,
            "properties": {k: _infer_property_schema(k, v) for k, v in value.items()},
        }
    return {"description": description}


def generate_draft_schema(payload, datamodel=None, subject=None):
    """Generate a draft schema.json from a sample payload, following the
    same structural conventions as a real Smart Data Models schema (allOf
    with the relevant common-schema.json definitions, the standard "type"
    enum property, required: [id, type]) so the output can be dropped into
    the existing contribution workflow with minimal editing -- not a bare
    JSON Schema fragment.

    Parameters:
        payload (dict): a sample key-values format payload.
        datamodel (str, optional): name for the entity type. Defaults to
            payload.get("type") or "MyEntity".
        subject (str, optional): subject name, used only in $id/title text.

    Returns:
        dict: a draft schema.json. Every description is a TODO placeholder
        -- a sample value can tell you a shape, never what it means.
    """
    datamodel = datamodel or payload.get("type") or "MyEntity"
    subject = subject or "dataModel.MySubject"

    allof = [{"$ref": f"{_COMMON_SCHEMA_URL}#/definitions/GSMA-Commons"}]
    covered = set(_GSMA_COMMONS_PROPERTIES)

    has_location_like = any(
        k in _LOCATION_COMMONS_PROPERTIES or _looks_like_geojson(v) for k, v in payload.items()
    )
    if has_location_like:
        allof.append({"$ref": f"{_COMMON_SCHEMA_URL}#/definitions/Location-Commons"})
        covered |= _LOCATION_COMMONS_PROPERTIES

    properties = {
        "type": {
            "type": "string",
            "enum": [datamodel],
            "description": f"Property. NGSI Entity type. It has to be {datamodel}",
        }
    }
    for key, value in payload.items():
        if key in ("id", "type") or key in covered:
            continue
        properties[key] = _infer_property_schema(key, value)

    allof.append({"properties": properties})

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$schemaVersion": "0.1.0",
        "$id": f"https://smart-data-models.github.io/{subject}/{datamodel}/schema.json",
        "title": f"{datamodel} - draft schema (auto-generated, not yet reviewed)",
        "description": "TODO: describe this entity type.",
        "modelTags": "",
        "type": "object",
        "allOf": allof,
        "required": ["id", "type"],
    }


def _looks_like_normalized_envelope(value):
    """True for a value shaped like an NGSI-v2 or NGSI-LD normalized
    attribute envelope: {"type": <tag>, "value": ...} or
    {"type": <tag>, "object": ...} (the Relationship form). Checking for
    "type" alongside "value"/"object" (rather than just "value" alone)
    keeps this from false-positiving on an ordinary nested JSON object
    that happens to have its own unrelated "value" key."""
    return isinstance(value, dict) and isinstance(value.get("type"), str) and ("value" in value or "object" in value)


def _is_normalized_payload(payload):
    """True if payload looks like NGSI-v2 or NGSI-LD normalized format
    rather than plain key-values -- checked by sampling its own attributes
    rather than assuming a format, since both flavors use the exact same
    envelope shape and "id"/"type" themselves are never wrapped in either
    format, so they can't be used to tell the two apart."""
    return any(
        _looks_like_normalized_envelope(v)
        for k, v in payload.items()
        if k not in ("id", "type", "@context")
    )


def _fetch_schema_content(schema_url):
    """Fetch and return the raw (unresolved $ref) schema.json content at a
    URL, or None if it can't be fetched. Deliberately not open_jsonref --
    that resolves every $ref into a much larger expanded tree, which
    wouldn't be comparable to generate_draft_schema's raw-$ref output."""
    try:
        response = requests.get(schema_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def identify_or_draft_datamodel(payload, fuzzy=False, fuzzy_threshold=0.3):
    """Identify whether a payload follows an existing Smart Data Model, or
    draft a new schema.json for it if not.

    Parameters:
        payload (dict): a sample payload in any of the three formats data
            space participants actually send -- plain key-values, NGSI-v2
            normalized ({"type": "Number", "value": ...}), or NGSI-LD
            normalized ({"type": "Property", "value"/"object": ...}).
            Auto-detected and flattened to key-values internally before
            identification, validation, or drafting, since all of those
            need to inspect actual attribute values, not envelopes.
        fuzzy (bool): when the payload's "type" doesn't match any known
            data model (or is missing), also try matching by attribute-name
            overlap against every known model. Off by default -- it's a
            noisy signal (see _fuzzy_match_candidates), not a reliable
            identification, so it's opt-in rather than silently guessing.
        fuzzy_threshold (float): minimum coverage score (0-1) for the fuzzy
            match's top candidate to be reported as a match instead of
            falling through to drafting a new schema.

    Returns:
        dict, always exactly {"schema", "candidates"}:

        schema (dict): {"content", "source", "datamodel", "subject", "url", "validation"}
            - content: the schema.json itself -- fetched from the matched
              model when source is "existing"/"existing_fuzzy", or the
              freshly generated draft when source is "generated".
            - source: "existing" (payload's "type" matched directly),
              "existing_fuzzy" (fuzzy match scored >= fuzzy_threshold), or
              "generated" (nothing matched -- content is a new draft).
            - confidence: only present when source is "existing_fuzzy" --
              the winning candidate's coverage score (0-1).
            - url: the real schema.json's URL, or None when generated.
            - validation: the validate_payload() result against the matched
              model, or None when generated. A "type" match doesn't
              guarantee the payload is actually valid for that model, so
              this is reported alongside rather than assumed.

        candidates (list): the fuzzy-match ranking ({"subject", "dataModel",
            "score"}, highest first). Populated whenever fuzzy=True was
            used to find/consider a match; empty otherwise. When source is
            "existing_fuzzy", the winning candidate is excluded (it's
            already described in "schema") -- these are the runner-ups.
    """
    if _is_normalized_payload(payload):
        payload = normalized2keyvalues_v2(payload)

    payload_type = payload.get("type")
    subjects = subject_for_datamodel(payload_type) if payload_type else False

    if subjects:
        subject = subjects[0]
        metadata = list_datamodel_metadata(payload_type, subject)
        schema_url = metadata["jsonSchemaUrl"] if metadata else None
        return {
            "schema": {
                "content": _fetch_schema_content(schema_url) if schema_url else None,
                "source": "existing",
                "datamodel": payload_type,
                "subject": subject,
                "url": schema_url,
                "validation": validate_payload(payload_type, subject, payload),
            },
            "candidates": [],
        }

    candidates = _fuzzy_match_candidates(payload.keys()) if fuzzy else []

    if candidates and candidates[0]["score"] >= fuzzy_threshold:
        top = candidates[0]
        metadata = list_datamodel_metadata(top["dataModel"], top["subject"])
        schema_url = metadata["jsonSchemaUrl"] if metadata else None
        return {
            "schema": {
                "content": _fetch_schema_content(schema_url) if schema_url else None,
                "source": "existing_fuzzy",
                "datamodel": top["dataModel"],
                "subject": top["subject"],
                "confidence": top["score"],
                "url": schema_url,
                "validation": validate_payload(top["dataModel"], top["subject"], payload),
            },
            "candidates": candidates[1:],
        }

    return {
        "schema": {
            "content": generate_draft_schema(payload),
            "source": "generated",
            "datamodel": payload.get("type") or "MyEntity",
            "subject": None,
            "url": None,
            "validation": None,
        },
        "candidates": candidates,
    }
