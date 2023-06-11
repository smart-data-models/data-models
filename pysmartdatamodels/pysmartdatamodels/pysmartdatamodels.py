
path = __file__

# Find the index of the last occurrence of /
index = path.rfind(os.sep)


# Extract the right part of the string up until the last /
left_part = path[:index]
# lookup install path for - model-assets

official_list_file_name = left_part + "/model-assets/official_list_data_models.json"
ddbb_attributes_file = left_part + "/model-assets/smartdatamodels.json"

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
    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
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
    import json

    output = []
    # Opens the file with the list of data models
    with open(ddbb_attributes_file, "r") as ddbb_attributes_file_pointer:
        output = json.load(ddbb_attributes_file_pointer)
    return output

# 3
def list_all_datamodels():
    """List the names of the entities defined in the data models.
    Parameters:

    Returns:
       array of strings: data models' names
    """
    import json

    output = []
    # Opens the file with the list of data models
    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
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
    import json

    output = []

    # Opens the file with the list of data models
    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
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
    import json

    output = []
    done = False

    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    output = []
    done = False

    # Access the full database of attributes and stores is in a dictionary
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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

    import sys
    import datetime

    import jsonschema
    import pytz
    import json
    from jsonschema import validate

    def open_jsonref(fileUrl):
        import jsonref
        import requests

        if fileUrl[0:4] == "http":
            # es URL
            try:
                pointer = requests.get(fileUrl)
                output = jsonref.loads(
                    pointer.content.decode("utf-8"), load_on_repr=False
                )
                return output
            except:
                return ""
        else:
            # es file
            try:
                file = open(fileUrl, "r")
                return jsonref.loads(file.read())
            except:
                return ""

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
                                    output[prop]["type"] = descriptionPiece
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

    def echo(concept, variable):
        print("*** " + concept + " ***")
        print(variable)
        print("--- " + concept + " ---")

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


# 12 print data models attributes


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
    import json

    output = []
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    with open(ddbb_attributes_file, "r") as ddbb_attributes_pointer:
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
    import json

    # output = []
    done = False

    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
        datamodelsdict = json.load(list_of_datamodels_pointer)["officialList"]
        for item in datamodelsdict:
            if "repoName" and "dataModels" in item:
                if item["repoName"] == subject:
                    output = item["repoLink"]
                    done = True
    if not done:
        output = False

    return output

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
    import json

    output = []
    done = False

    with open(official_list_file_name, "r") as list_of_datamodels_pointer:
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

def update_data():
    import os
    import urllib.request

    data_dir = os.path.join(os.path.dirname(__file__), "model-assets")

    # Download the latest data files from a remote server
    urllib.request.urlretrieve("https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json", os.path.join(data_dir, "official_list_data_models.json"))
    urllib.request.urlretrieve("https://smartdatamodels.org/extra/smartdatamodels.json", os.path.join(data_dir, "smartdatamodels.json"))

    # Update the data files with the latest information
    # (This will depend on the specific data files and the format they use)

