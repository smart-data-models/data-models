import os
import re
import json

import sys
import datetime

import jsonschema
import pytz
from jsonschema import validate
import requests

import urllib.request
# from utils.common_utils import *
from .utils import extract_subject_from_raw_url, extract_datamodel_from_raw_url, \
                    open_jsonref, parse_property, normalized2keyvalues, create_context, \
                    generate_random_string, is_metadata_properly_reported, is_metadata_existed, \
                    schema_output_sum, message_after_check_schema

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

    def parse_description(schemaPayload):
        output = {}
        purgedDescription = str(schemaPayload["description"]).replace(chr(34), "")
        # process the description
        purgedDescription = re.sub(r'\.([A-Z])', r'. \1', purgedDescription)
        
        separatedDescription = purgedDescription. split(". ")
        copiedDescription = list.copy(separatedDescription)
        
        for descriptionPiece in separatedDescription:
            if descriptionPiece in propertyTypes:
                output["type"] = descriptionPiece
                copiedDescription.remove(descriptionPiece)
            elif descriptionPiece.find("Model:") > -1:
                copiedDescription.remove(descriptionPiece)
                output["model"] = descriptionPiece.replace("'", "").replace(
                        "Model:", "")

            if descriptionPiece.find("Units:") > -1:
                copiedDescription.remove(descriptionPiece)
                output["units"] = descriptionPiece.replace("'", "").replace(
                        "Units:", "")
        description = ". ".join(copiedDescription)

        return output, description

    def merge_duplicate_attributes(aa, bb):
        for key, values in bb.items():
            if key in aa:
                aa[key].extend(values)
            else:
                aa[key] = values
        return aa

    def parse_payload_v2(schemaPayload, level):
        output = {}
        attributes = {level: []}
        if level == 1:
            if "allOf" in schemaPayload:
                for index in range(len(schemaPayload["allOf"])):
                    if "definitions" in schemaPayload["allOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index]["definitions"], level + 1)
                        output = dict(output, **partialOutput)
                    elif "properties" in schemaPayload["allOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index], level + 1)
                        output = dict(output, **partialOutput["properties"])
                    else:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index], level + 1)
                        output = dict(output, **partialOutput)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)
            if "anyOf" in schemaPayload:
                for index in range(len(schemaPayload["anyOf"])):
                    if "definitions" in schemaPayload["anyOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index]["definitions"], level + 1)
                        output = dict(output, **partialOutput)
                    elif "properties" in schemaPayload["anyOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index], level + 1)
                        output = dict(output, **partialOutput["properties"])
                    else:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index], level + 1)
                        output = dict(output, **partialOutput)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)
            if "oneOf" in schemaPayload:
                for index in range(len(schemaPayload["oneOf"])):
                    if "definitions" in schemaPayload["oneOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index]["definitions"], level + 1)
                        output = dict(output, **partialOutput)
                    elif "properties" in schemaPayload["oneOf"][index]:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index], level + 1)
                        output = dict(output, **partialOutput["properties"])
                    else:
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index], level + 1)
                        output = dict(output, **partialOutput)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)

            if "properties" in schemaPayload:
                output, partialAttr = parse_payload_v2(schemaPayload["properties"], level + 1)
                attributes = merge_duplicate_attributes(attributes, partialAttr)
                    
        elif level < 8:
            if isinstance(schemaPayload, dict):
                for subschema in schemaPayload:
                    if subschema in ["allOf", "anyOf", "oneOf"]:
                        output[subschema] = []
                        for index in range(len(schemaPayload[subschema])):
                            if "properties" in schemaPayload[subschema][index]:
                                partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][index], level + 1)
                                output[subschema].append(partialOutput["properties"])
                            else:
                                partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][index], level + 1)
                                output[subschema].append(partialOutput)
                            attributes = merge_duplicate_attributes(attributes, partialAttr)

                    elif subschema == "properties":
                        output[subschema] = {}
                        for prop in schemaPayload["properties"]:
                            try:
                                output[subschema][prop]
                            except:
                                output[subschema][prop] = {}
                                attributes[level].append(prop)
                            for item in list(schemaPayload["properties"][prop]):
                                if item in ["allOf", "anyOf", "oneOf"]:
                                    output[subschema][prop][item] = []
                                    for index in range(len(schemaPayload[subschema][prop][item])):
                                        partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item][index], level + 1)
                                        output[subschema][prop][item].append(partialOutput)
                                        attributes = merge_duplicate_attributes(attributes, partialAttr)
                                elif item == "description":
                                    # print("Detectada la descripcion de la propiedad=" + prop)
                                    x_ngsi, description = parse_description(schemaPayload[subschema][prop])
                                    output[subschema][prop][item] = description
                                    if x_ngsi:
                                        output[subschema][prop]["x-ngsi"] = x_ngsi
                                
                                elif item == "items":
                                    output[subschema][prop][item], partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item], level + 1)
                                    attributes = merge_duplicate_attributes(attributes, partialAttr)
                                elif item == "properties":
                                    output[subschema][prop][item], partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item], level + 1)
                                    attributes = merge_duplicate_attributes(attributes, partialAttr)
                                elif item == "type":
                                    if schemaPayload[subschema][prop][item] == "integer":
                                        output[subschema][prop][item] = "number"
                                    else:
                                        output[subschema][prop][item] = schemaPayload[subschema][prop][item]
                                else:
                                    output[subschema][prop][item] = schemaPayload[subschema][prop][item]

                    elif isinstance(schemaPayload[subschema], dict):        
                        attributes[level].append(subschema)     
                        output[subschema], partialAttr = parse_payload_v2(schemaPayload[subschema], level + 1)
                        attributes = merge_duplicate_attributes(attributes, partialAttr)
                    else:
                        if subschema == "description":
                            x_ngsi, description = parse_description(schemaPayload)
                            output[subschema] = description
                            if x_ngsi:
                                output["x-ngsi"] = x_ngsi
                        else:
                            output[subschema] = schemaPayload[subschema]
            
            elif isinstance(schemaPayload, list):
                for index in range(len(schemaPayload)):
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload[index], level + 1)
                    output = dict(output, **partialOutput)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)
        else:
            return None, None

        return output, attributes

    def parse_yamlDict(yamlDict, datamodelRepoUrl, level):

        output = {}
        if isinstance(yamlDict, list):
            for item in yamlDict:
                partialoutput = parse_yamlDict(item, datamodelRepoUrl, level+1)
                output = dict(output, **partialoutput)
        else:
            for prop in yamlDict:
                # print("prop ", prop)

                if prop == "id": continue

                if isinstance(yamlDict[prop], list) and len(yamlDict[prop]) > 1 and isinstance(yamlDict[prop][0], dict):
                    for item in yamlDict[prop]:
                        partialoutput = parse_yamlDict(item, datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
        
                if isinstance(yamlDict[prop], dict):
                    if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                        partialoutput = parse_yamlDict(yamlDict[prop], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
                        continue
                    # print("dict prop ", prop)
                    propKeys = list(yamlDict[prop].keys())

                    # if there's type, and there's no items, allOf, properties
                    # if type is a 
                    if isinstance(yamlDict[prop], dict) and prop != "x-ngsi" and not prop in exceptions:
                        # print("++++ context prop ", prop)
                        
                        try:
                            propertyType = yamlDict[prop]["x-ngsi"]["type"]
                            if propertyType in propertyTypes:
                                # print(propertyType)
                                # print(propertyTypes)
                                output[prop] = {}
                                output[prop]["x-ngsi"] = True
                                output[prop]["x-ngsi_text"] = "ok to " + str(propertyType)
                            else:
                                output[prop]["x-ngsi"] = False
                                output[prop]["x-ngsi_text"] = "Wrong NGSI type of " + propertyType + " in the description of the property on level " + str(level)
                        except:
                            output[prop] = {}
                            output[prop]["x-ngsi"] = False
                            output[prop]["x-ngsi_text"] = "Missing NGSI type of " + str(propertyTypes) + " in the description of the property on level " + str(level)

                        # checking the pure description
                        try:
                            description = yamlDict[prop]["description"]
                            if len(description) > 15:
                                # No double quotes in the middle
                                # if not (".." in description):
                                    # If there is a link, check that the link is valid
                                output[prop]["documented"] = True
                                output[prop]["text"] = description
                                # else:
                                #     output[key]["documented"] = False
                                #     output[key]["text"] = doubleDotsDescription
                            else:
                                output[prop]["documented"] = False
                                output[prop]["text"] = incompleteDescription
                        except:
                            # output[key] = {}
                            output[prop]["documented"] = False
                            output[prop]["text"] = withoutDescription

                        # Type property matches data model name
                        if prop == "type" and level == 1:
                            try:
                                propertyType = yamlDict[prop]["enum"]
                                if propertyType[0] == extract_datamodel_from_raw_url(datamodelRepoUrl):
                                    output[prop]["type_specific"] = True
                                    output[prop]["type_specific_text"] = "Type property matches to data model name on level " + str(level)
                                else:
                                    output[prop]["type_specific"] = False
                                    output[prop]["type_specific_text"] = "Type property doesn't match to data model name on level " + str(level)
                            except:
                                output[prop]["type_specific"] = False
                                output[prop]["type_specific_text"] = "Missing Type property"
                    
                    if "properties" in propKeys:
                        partialoutput = parse_yamlDict(yamlDict[prop]["properties"], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
                    if "items" in propKeys and yamlDict[prop]["items"]:
                        if isinstance(yamlDict[prop]["items"], list):
                            for index in range(len(yamlDict[prop]["items"])):
                                partialoutput = parse_yamlDict(yamlDict[prop]["items"][index], datamodelRepoUrl, level+1)
                                output = dict(output, **partialoutput)
                        else:
                            partialoutput = parse_yamlDict(yamlDict[prop]["items"], datamodelRepoUrl, level+1)
                            output = dict(output, **partialoutput)
                    if "anyOf" in propKeys:
                        partialoutput = parse_yamlDict(yamlDict[prop]["anyOf"], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
                    if "allOf" in propKeys:
                        partialoutput = parse_yamlDict(yamlDict[prop]["allOf"], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
                    if "oneOf" in propKeys:
                        partialoutput = parse_yamlDict(yamlDict[prop]["oneOf"], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput) 

        return output

    def is_property_already_existd(output, yamlDict):
        try:
            commonProperties =["id", "name", "description", "location", "seeAlso", "dateCreated", "dateModified", "source", "alternateName", "dataProvider", "owner", "address", "areaServed", "type"]
            existing = "alreadyUsedProperties"
            available = "availableProperties"

            #print("llego a la funcion")
            output[existing] = []
            output[available] = []

            for key in yamlDict:
                if key in commonProperties:
                    continue
                #print(key)
                lowKey = key.lower()

                with open(ddbb_attributes_file, "r", encoding='utf-8') as ddbb_attributes_pointer:
                    datamodelsdict = json.load(ddbb_attributes_pointer)

                results = []
                for item in datamodelsdict:
                    # print(item)
                    try:
                        if re.match(lowKey, item['property'], re.IGNORECASE):
                            results.append(item)
                    except:
                        nada = 0

                # print(results)
                if len(results) > 0:
                    definitions= []
                    dataModelsList = []
                    types = []
                    for index, item in enumerate(results):
                        dataModelsList.append(str(index + 1) + ".-" + item["dataModel"])
                        #print(item["type"])
                        if "description" in item or "type" in item:
                            if "description" in item:
                                definitions.append(str(index + 1) + ".-" + item["description"])
                            else:
                                definitions.append(str(index + 1) + ".- missing description")
                            if "type" in item:
                                types.append(str(index + 1) + ".-" +  item["type"])
                            else:
                                types.append(str(index + 1) + ".- missing type")
                        else:
                            output[existing].append({"Error": lowKey})
                    output[existing].append({key: "Already used in data models: " + ",".join(dataModelsList) + " with these definitions: " + chr(13).join(definitions) + " and these data types: " + ",".join(types)})
                else:
                    output[available].append({key: "Available"})

        except:
            output[existing].append({"Error": lowKey})
        
        return output

    # initialize variables for the script
    output = {}  # the json answering the test
    tz = pytz.timezone("Europe/Madrid")
    # metaSchema = open_jsonref("https://json-schema.org/draft/2019-09/hyper-schema")
    metaSchema = open_jsonref("https://json-schema.org/draft/2020-12/meta/validation")
    propertyTypes = ["Property", "Relationship", "GeoProperty"]
    incompleteDescription = "Incomplete description"
    withoutDescription = "No description at all"
    doubleDotsDescription = "Double dots in the middle"
    wrongTypeDescription = "Wrong NGSI types"
    missingTypeDescription = "Missing NGSI types"
    exceptions = ["coordinates", "bbox", "type"]

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
        yamlDict, attributes = parse_payload_v2(schema, 1)
    except:
        output["result"] = False
        output["cause"] = "schema cannot be loaded (possibly invalid $ref)"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        sys.exit()
    # echo("yamlDict", yamlDict)

    # check the duplicated attributes
    if len(attributes[2]) != len(set(attributes[2])):

        def find_duplicates(input_list):
            """
            Find and output the duplicated values inside a list.
            Args:
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

        output["cause"] = f"Duplicated attributes (User-defined properties is duplicated with system-defined properties):\n\t{', '.join(find_duplicates(attributes[2]))}"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schema_url": schema_url}
        print(json.dumps(output))
        sys.exit()

    output[documented] = parse_yamlDict(yamlDict, schema_url, 1)
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
    # TODO
    output = is_property_already_existd(output, yamlDict)

    # now it checks if the metadata is properly reported
    output = is_metadata_properly_reported(output, schemaDict)

    # now it checks if the metadata does exist
    output = is_metadata_existed(output, schemaDict, schema_url, message="schema")

    # make a summary of all the output
    results = schema_output_sum(output)
    print(message_after_check_schema(results))

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
                            print(f"Failed to update entity with nonexistent attribute. Status code: {create_response.status_code}.")
                            print(create_response.text)
                            return False

                    except requests.exceptions.RequestException as e:
                        print(f"Failed to update entity with nonexistent attribute: {e}")
                        return False
                else:
                    print(f"Failed to update entity. Trying to update nonexistent attributes. If so, set updateThenCreate to true.")
                    return False
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
                