################################################################################
#  Licensed to the FIWARE Foundation (FF) under one
#  or more contributor license agreements. The FF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  for questions address it to alberto.abella@fiware.org
################################################################################

import json
import sys
import rstr
import string
import random
import requests

from validator_collection import checkers

from faker import Faker
fake = Faker()

pendingToImplement = "Version 0.1 not implemented"
missingEntity = "Missing entity name"

newline = "\n  "
newsubline = "\n   "
KEYWORDS_FOR_CERTAIN_CHECK = "smart-data-models"
CHECKED_PROPERTY_CASES = ['well documented', 'already used', 'newly available', 'Metadata', 'Failed']

def is_url_existed(url, message=""):
    output = []
    try:
        pointer = requests.get(url)
        if pointer.status_code == 200:
            return [True, pointer.text]
        else:
            return [False, pointer.status_code]
    except:
        return [False, "wrong domain"]


def extract_datamodel_from_raw_url(schemaUrl):
    """It returns the name of the data model given the schema repository url
    """
    import re
    patternRaw = "https:\/\/raw\.githubusercontent\.com\/smart\-data\-models\/.*\/(.*)\/schema\.json"
    patternPage = "https:\/\/smart-data-models\.github\.io\/.*\/(.*)\/schema\.json"
    urlSearch = re.search(patternRaw, schemaUrl, re.IGNORECASE)
    url2Search = re.search(patternPage, schemaUrl, re.IGNORECASE)
    if urlSearch:
        dataModel = urlSearch.group(1)
    elif url2Search:
        dataModel = url2Search.group(1)
    else:
        dataModel = "dataModel"
    return dataModel


def extract_subject_from_raw_url(schemaUrl):
    """It returns the name of the subject given the schema repository url
    """
    import re
    patternRaw = "https:\/\/raw\.githubusercontent\.com\/smart\-data\-models\/(.*)\/.*\/schema\.json"
    patternPage = "https:\/\/smart-data-models\.github\.io\/(.*)\/.*\/schema\.json"
    urlSearch = re.search(patternRaw, schemaUrl, re.IGNORECASE)
    url2Search = re.search(patternPage, schemaUrl, re.IGNORECASE)
    if urlSearch:
        subject = urlSearch.group(1).split("/")[0]
    elif url2Search:
        subject = url2Search.group(1).split("/")[0]
    else:
        subject = "subject"
    return subject


def open_jsonref(fileUrl):
    """It opens the json file given the url or path, returns empty string if not reachable
    """
    import jsonref
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True, merge_props=True)
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
        
        
def normalized2keyvalues(normalizedPayload):
    """It returns the key value format by given the normalized format json payload
    """
    import json

    normalizedDict = normalizedPayload
    output = {}
    # print(normalizedDict)
    for element in normalizedDict:
        # print(normalizedDict[element])
        try:
            if "value" in normalizedDict[element]:
                value = normalizedDict[element]["value"]
                if "@type" in value:
                    output[element] = normalizedDict[element]["value"]["@value"]
                else:
                    output[element] = value
            else:
                output[element] = normalizedDict[element]
        except:
            output[element] = normalizedDict[element]

    # print(output)
    return output


def create_context(subject):
    """It returns the context uri of given subject
    """
    return "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/context.jsonld"


def generate_random_string(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

########################################
#   Generate fake example related
########################################

def fake_uri(propertyName, dataModel):
    output = "urn:ngsi-ld:" + str(dataModel) + ":" + str(propertyName) + ":"
    output += fake.bothify(text="????:########", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # genera example uri
    return output

def payload_uri(propertyName, dataModel):
    return {"type": "Property", "value": fake_uri(propertyName, dataModel)}

def payload_relationship(propertyName, dataModel):
    return {"type": "object", "value": fake_uri(propertyName, dataModel)}

def fake_geoproperty(type):
    dictValue = {}
    if type == "Point":
        dictValue = {"type": type, "coordinates": [float(fake.latitude()), float(fake.longitude())]}
    elif type == "LineString":
        dictValue = {"type": type, "coordinates": [[float(fake.latitude()), float(fake.longitude())],
                                                            [float(fake.latitude()), float(fake.longitude())]]}
    elif type == "Polygon":
        dictValue = {"type": type, "coordinates": [[float(fake.latitude()), float(fake.longitude())],
                                                            [float(fake.latitude()), float(fake.longitude())],
                                                            [float(fake.latitude()), float(fake.longitude())],
                                                            [float(fake.latitude()), float(fake.longitude())]]}
    return dictValue

def payload_geoproperty(type):
    return {"type": "Property", "value": fake_geoproperty(type)}

def fake_number(*args):
    Faker.seed()
    # expect a tuple with (left_digits, min, max)
    # if there is a maximum a minimum should be included
    # otherwise it throws an error
    # print(type(args))
    # print(type(args[0]))
    if isinstance(args[0], int):
        minimum = 0
        maximum = 1000
        leftDigits = 6
    else:
        leftDigits = int(args[0][0])
        if len(args[0]) > 1:
            minimum = int(args[0][1])
        else:
            minimum = 0
        if len(args[0]) > 2:
            maximum = int(args[0][2])
        else:
            maximum = max(1000, minimum + 1000)
    return fake.pyfloat(left_digits=leftDigits, right_digits=1, min_value=minimum, max_value=maximum)

def fake_integer(*args):
    Faker.seed()
    # expect a tuple with (min, max)
    # if there is a maximum a minimum should be included
    # otherwise it throws an error
    # print(type(args))
    # print(type(args[0]))
    if isinstance(args[0], int):
        minimum = 0
        maximum = 1000
    else:
        if len(args[0]) > 0:
            minimum = int(args[0][0])
        else:
            minimum = 0
        if len(args[0]) > 1:
            maximum = int(args[0][1])
        else:
            maximum = max(1000, minimum + 1000)
    return fake.pyint(minimum, maximum)

def payload_number(*args):
    return {"type": "Property", "value": fake_number(*args)}

def payload_integer(*args):
    return {"type": "Property", "value": fake_integer(*args)}

def fake_time():
    return fake.time(pattern='%H:%M:%SZ')

def fake_date():
    # genera example date
    return fake.date(pattern='%Y-%m-%dT%H:%M:%SZ', end_datetime=None)

def payload_time():
    return {"type": "Property", "value": {"@type": "Time", "@value": fake_time()}}

def payload_date():
    return {"type": "Property", "value": {"@type": "DateTime", "@value": fake_date()}}

def fake_email(dataModel):
    list_of_domains = (
        'com',
        'com.br',
        'net',
        'net.br',
        'org',
        'org.br',
        'gov',
        'gov.br'
    )

    dns_org = fake.random_choices(
        elements=list_of_domains,
        length=1
    )[0]

    return f"{fake.first_name()}.{fake.last_name()}@{dataModel}.{dns_org}".lower()

def payload_email(dataModel):
    return {"type": "Property", "value": fake_email(dataModel)}

def fake_string(length):
    # genera example string (regular)
    if length == 1:
        return fake.paragraphs(nb=length)[0]
    else:
        return fake.paragraphs(nb=length)

def payload_string(length):
    return {"type": "Property", "value": fake_string(length)}

def fake_enum(elementsList, length):
    if length == 1:
        return fake.random_choices(elements=elementsList, length=length)[0]
    else:
        return fake.random_choices(elements=elementsList, length=length)

def payload_enum(elementsList, length):
    return {"type": "Property", "value": fake_enum(elementsList, length)}

def fake_boolean():
    # because False in python starts with capital letter
    return fake.random_choices(elements=[True, False], length=1)[0]

def payload_boolean():
    return {"type": "Property", "value": fake_boolean()}

def parse_schema_description(description):
    # it returns an array of this format
    # [description, Property/Relationship/Geoproperty, Model, Units, Enum, Privacy]
    output = ["", "", "", "", "", ""]
    propertyTypes = ["Property", "Relationship", "Geoproperty"]
    splittedDescription = description.split(". ")
    # print(splittedDescription)
    aggregatedDescription = []

    for item in splittedDescription:
        if item in propertyTypes:
            output[1] = item
        elif "Model:" in item:
            output[2] = (item.replace("'", ""))[len("Model:"):]
        elif "Units:" in item:
            output[3] = (item.replace("'", ""))[len("Units:"):]
        elif "Enum:" in item:
            raw = (item.replace("'", ""))[len("Enum:"):]
            output[4] = raw.split(", ")
        elif "Privacy:" in item:
            output[5] = (item.replace("'", ""))[len("Privacy:"):]
        else:
            aggregatedDescription.append(item)
    output[0] = ". ".join(aggregatedDescription)
    return output

def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")

def fake_array(type, numItems, options):
    # type can be number, boolean, string, date-time, enum, array
    # options for type number is a tuple with (length, minimum and maximum)
    # options for type string is an integer with the length in paragraphs
    # options for type enum is the list with the possible values
    # options for array is a list with two values [type for the items, options for this type of item]
    # options for object is the complete payload

    if type == "number":
        return [fake_number(options) for i in range(numItems)]
    elif type == "boolean":
        return [fake_boolean() for i in range(numItems)]
    elif type == "string":
        return [fake_string(options) for i in range(numItems)]
    elif type == "date-time":
        return [fake_date() for i in range(numItems)]
    elif type == "enum":
        return [fake_enum(options) for i in range(numItems)]
    elif type == "array":
        return pendingToImplement
    elif type == "object":
        return pendingToImplement

def payload_array(type, numItems, options):
    if type != "array" and type != "object":
        return {"type": "Property", "value": fake_array(type, numItems, options)}
    else:
        return pendingToImplement

def parse_property(fullPayload, dataModel, level):
    # echo("payload", fullPayload)
    prop = [p for p in fullPayload.keys()][0]
    # echo("prop", prop)
    payload = fullPayload[prop]

    keys = [k for k in payload]
    # echo("keys", keys)
    if "required" in keys:
        del fullPayload[prop]["required"]

    if "description" in keys:
        # [description, Property/Relationship/Geoproperty, Model, Units, Enum, Privacy]
        metadata = parse_schema_description(payload["description"])
    else:
        metadata = ["", "Property"]
    if prop == "id" and level == 0:
        return {"id": fake_uri("id", dataModel)}
    elif prop == "id" and level > 0:
        return payload_uri("id", "id")
    elif "patternProperties" in keys:
        # print("Detected patternProperties")
        keyPatterned = list(payload["patternProperties"].keys())[0]
        propertyName = rstr.xeger(keyPatterned)
        # print(keyPatterned, propertyName)
        # print(fullPayload)
        if "required" in fullPayload[prop]:
            del fullPayload[prop]["required"]
        return parse_property({propertyName: fullPayload[prop]["patternProperties"][keyPatterned]}, dataModel, level+1)
    elif prop == "type" and level == 0:
        if "enum" in fullPayload[prop]:
            return fullPayload[prop]["enum"][0]
        else:
            return missingEntity
    elif prop == "location":
        return payload_geoproperty("Point")
    elif metadata[1] == "Relationship":
        return payload_relationship(prop, dataModel)
    elif metadata[1] == "Geoproperty":
        return payload_geoproperty("Point")
    elif prop in ["anyOf", "allOf", "oneOf"]:
        return parse_property({"item": fullPayload[prop][0]}, dataModel, level)
    elif "type" in keys:
        if payload["type"] == "number":
            argsNumber = (4,)
            ### treating number with/without maximum/minimum ###
            if "minimum" in payload:
                argsNumber = argsNumber + (float(payload["minimum"]),)
            else:
                argsNumber = argsNumber + (0,)
            if "maximum" in payload:
                argsNumber = argsNumber + (float(payload["maximum"]),)
            else:
                argsNumber = argsNumber + (max(1000, argsNumber[1] + 1000),)
            return payload_number(argsNumber)
        elif payload["type"] == "integer":
            argsNumber = ()
            ### treating number with/without maximum/minimum ###
            if "minimum" in payload:
                argsNumber = argsNumber + (int(payload["minimum"]),)
            else:
                argsNumber = argsNumber + (0,)
            if "maximum" in payload:
                argsNumber = argsNumber + (int(payload["maximum"]),)
            else:
                argsNumber = argsNumber + (int(argsNumber[0] + 1000),)
            return payload_integer(argsNumber)
        elif payload["type"] == "string" and "format" in keys:
            if (payload["format"] == "date-time") or (payload["format"] == "date"):
                return payload_date()
            elif payload["format"] == "time":
                return payload_time()
            elif payload["format"] == "uri":
                return payload_uri(prop, dataModel)
            elif (payload["format"] == "idn-email") or (payload["format"] == "email"):
                return payload_email(dataModel)
            elif payload["format"] == "text":
                return payload_string(1)
        elif payload["type"] == "string" and "enum" in keys:
            return payload_enum(payload["enum"], 1)
        elif payload["type"] == "string":
            return payload_string(1)
        elif payload["type"] == "boolean":
            return payload_boolean()
        elif payload["type"] == "array":
            if "minItems" in payload:
                arrayItems = payload["minItems"]
            else:
                arrayItems = 2
            if "maxItems" in payload:
                arrayItems = int((arrayItems + int(payload["maxItems"]))/2)
            else:
                arrayItems = arrayItems
            arrayPayload = payload["items"].copy()
            if "required" in arrayPayload:
                del arrayPayload["required"]
            valuesArray = [parse_property({"items": arrayPayload}, dataModel, level+1)["value"] for i in range(arrayItems)]
            return {"type": "Property", "value": valuesArray}
        elif payload["type"] == "object":
            # print("parsing object")
            valuesObject = {}
            # print(payload)
            objectPayload = payload["properties"]
            if "required" in objectPayload:
                del objectPayload["required"]
            for p in objectPayload:
                # echo("{prop: payload[properties]}", {p: payload["properties"][p]})
                if p != "required":
                    valuesObject[p] = parse_property({p: payload["properties"][p]}, dataModel, level+1)["value"]

            return {"type": "Property", "value": valuesObject}
    elif "oneOf" in keys:
        return parse_property({prop: fullPayload[prop]["oneOf"][0]}, dataModel, level)
    else:
        return {prop: pendingToImplement, "value": fake_uri(prop, dataModel)}


def is_metadata_properly_reported(output, schemaDict):
    try:
        metadata = "metadata"
        output[metadata] = {}
        if "derivedFrom" in schemaDict:
            derivedFrom = schemaDict["derivedFrom"]
            if derivedFrom != "":
                # check that it is a valid url
                if not checkers.is_url(derivedFrom):
                    output["metadata"]["derivedFrom"] = {"warning": "derivedFrom is not a valid url"}
                else:
                    if not is_url_existed(derivedFrom)[0]:
                        output["metadata"]["derivedFrom"] = {"warning": "derivedFrom url is not reachable"}
        else:
            output["metadata"]["derivedFrom"] = {"warning": "not derivedFrom clause, include derivedFrom = '' in the header"}
    except:
        output["metadata"]["derivedFrom"] = {"warning": "not possible to check derivedFrom clause, Does it exist a derivedFrom = '' clause in the header?"}

    # check that the header license is properly reported
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "license" in schemaDict:
            license = schemaDict["license"]
            if license != "":
                # check that it is a valid url
                if not checkers.is_url(license):
                    output["metadata"]["license"] = {"warning": "License is not a valid url. It should be a link to the license document"}
                else:
                    if not is_url_existed(license)[0]:
                        output["metadata"]["license"] = {"warning": "license url is not reachable"}
            else:
                output["metadata"]["license"] = {"warning": "license is empty, include a license = '' in the header "}
        else:
            output["metadata"]["license"] = {"warning": "not license clause, does it exist a license = '' in the header?"}
    except:
        output["metadata"]["license"] = {"warning": "not possible to check license clause"}

    return output

def is_metadata_existed(output, jsonDict, schemaUrl, message="", checkall=True, checklist=None):

    # if checkall is True, then ignore checklist
    # if checkall is False, then checklist will be used

    # if not checkall:
        # ["$schema", "$id", "title", "", "description", "tags", "version", "required clause"]

    # check that the "$schema" exist, by default is "http://json-schema.org/schema"
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$schema" in jsonDict:
            schema = jsonDict["$schema"]
            if schema == "":
                output["metadata"]["$schema"] = {"warning": "$schema is empty"}
            elif not isinstance(schema, str):
                output["metadata"]["$schema"] = {"warning": "$schema is not a string"}
            # 
            elif schema != "http://json-schema.org/schema#":
                output["metadata"]["$schema"] = {"warning": "$schema should be \"http://json-schema.org/schema#\" by default"}
        else:
            output["metadata"]["$schema"] = {"warning": "Missing $schema clause, include $schema = '' in the header"}
    except:
        output["metadata"]["$schema"] = {"warning": "not possible to check $schema clause, Does it exist a $schema = '' in the header?"}

    # check that the "$id" exist
    try:
        # print(jsonDict)
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$id" in jsonDict:
            # print("-----------")
            id = jsonDict["$id"]
            if id == "":
                output["metadata"]["$id"] = {"warning": "$id is empty"}
            elif not isinstance(id, str):
                output["metadata"]["$id"] = {"warning": "$id is not a string"}
            # https://smart-data-models.github.io/dataModel.DataQuality/DataQualityAssessment/schema.json
            elif (KEYWORDS_FOR_CERTAIN_CHECK in schemaUrl) and (id != schemaUrl):
                output["metadata"]["$id"] = {"warning": "$id doesn't match, please check it again"}
        else:
            output["metadata"]["$id"] = {"warning": "Missing $id clause, include $id = '' in the header"}
    except:
        output["metadata"]["$id"] = {"warning": "not possible to check $id clause, Does it exist a $id = '' in the header?"}
    
    # check that the title exist
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "title" in jsonDict:
            title = jsonDict["title"]
            if title == "":
                output["metadata"]["title"] = {"warning": "Title is empty"}
            elif not isinstance(title, str):
                output["metadata"]["title"] = {"warning": "Title is not a string"}
            elif len(title) < 15:
                output["metadata"]["title"] = {"warning": "Title too short"}
        else:
            output["metadata"]["title"] = {"warning": "Missing title clause, include title = '' in the header"}
    except:
        output["metadata"]["title"] = {"warning": "not possible to check title clause, Does it exist a title = '' in the header?"}

    # check that the description exists
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "description" in jsonDict:
            description = jsonDict["description"]
            if description == "":
                output["metadata"]["description"] = {"warning": "Description is empty"}
            elif not isinstance(description, str):
                output["metadata"]["description"] = {"warning": "Description is not a string"}
            elif len(description) < 34:
                output["metadata"]["description"] = {"warning": "Description is too short"}
        else:
            output["metadata"]["description"] = {"warning": "Missing description clause, include description = '' in the header"}
    except:
        output["metadata"]["description"] = {"warning": "not possible to check description clause, does it exist a description = '' in the header?"}

    # check that the tags exist
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "modelTags" in jsonDict:
            modelTags = jsonDict["modelTags"]
            if modelTags == "":
                output["metadata"]["modelTags"] = {"warning": "modelTags is empty"}
            elif not isinstance(title, str):
                output["metadata"]["modelTags"] = {"warning": "modelTags is not a string"}
        else:
            output["metadata"]["modelTags"] = {"warning": "Missing modelTags clause, , include modelTags = '' in the header"}
    except:
        output["metadata"]["modelTags"] = {"warning": "not possible to check modelTags clause, does it exit a modelTags = '' in the header?"}

    # check that the version exists
    try:
        import re
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$schemaVersion" in jsonDict:
            schemaVersion = jsonDict["$schemaVersion"]
            pattern = "^\d{1,3}.\d{1,3}.\d{1,3}$"
            if schemaVersion == "":
                output["metadata"]["schemaVersion"] = {"warning": "missing $schemaVersion, include the value. Default = 0.0.1"}
            elif not isinstance(schemaVersion, str):
                output["metadata"]["schemaVersion"] = {"warning": "$schemaVersion is not a string"}
            elif re.search(pattern, schemaVersion) is None:
                output["metadata"]["schemaVersion"] = {"warning": "Schema version format wrong. Right is x.x.x"}
        else:
            output["metadata"]["schemaVersion"] = {"warning": "Missing schemaVersion clause, include $schemaVersion = '' in the header "}
    except:
        output["metadata"]["schemaVersion"] = {"warning": "not possible to check schemaVersion clause, does it exist a $schemaVersion = '' in the header?"}

    # check that the required clause exists
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "required" in jsonDict:
            required = jsonDict["required"]
            # print(required)
            # print(type(required))
            if required == "":
                output["metadata"]["required"] = {"warning": "missing required, include the values. Default = ['id', 'type]"}
            elif not isinstance(required, list):
                output["metadata"]["required"] = {"warning": "required is not a list"}
            elif ("id" not in required) or ("type" not in required):
                output["metadata"]["required"] = {"warning": "id and type are mandatory"}
            elif len(required) > 4:
                output["metadata"]["required"] = {"warning": "Too many required attributes, consider its reduction to less than 5 preferably just id and type"}
        else:
            output["metadata"]["required"] = {"warning": "Missing required clause, include required = ['id', 'type']"}
    except:
        output["metadata"]["required"] = {"warning": "not possible to check required clause, does it exist a required = ['id', 'type']?"}

    return output


def schema_output_sum(output):

    documentationStatusOfProperties = output['documentationStatusOfProperties']
    alreadyUsedProperties = output['alreadyUsedProperties']
    availableProperties = output['availableProperties']
    metadata = output['metadata']

    results = {}
    results = {key: [] for key in CHECKED_PROPERTY_CASES}
    results['Failed'] = {}

    for pp, value in documentationStatusOfProperties.items():
        if value['documented'] & value['x-ngsi']:
            results['well documented'].append(pp)
        elif value['x-ngsi'] is False:
            if value['x-ngsi_text'] not in results['Failed'].keys():
                results['Failed'][value['x-ngsi_text']] = []
            results['Failed'][value['x-ngsi_text']].append(pp)
        elif value['documented'] is False:
            if value['text'] not in results['Failed'].keys():
                results['Failed'][value['text']] = []
            results['Failed'][value['text']].append(pp)
        if (pp == "type") and (value["type_specific"] is False):
            results['Failed'][value["type_specific_text"]] = []
            results['Failed'][value["type_specific_text"]].append(pp)
        if 'duplicated_prop' in value:
            try:
                results['Failed'][value['duplicated_prop_text']].append(pp)
            except:
                results['Failed'][value['duplicated_prop_text']] = []
                results['Failed'][value['duplicated_prop_text']].append(pp)

    for pp in alreadyUsedProperties:
        # print(pp.keys())
        results['already used'].append(list(pp.keys())[0])

    for pp in availableProperties:
        results['newly available'].append(list(pp.keys())[0])

    for pp, value in metadata.items():
        results['Metadata'].append(value['warning'])

    return results


def message_after_check_schema(results):
    message = ""
    for key in CHECKED_PROPERTY_CASES[:-2]:
        if len(results[key]) != 0:
            msg = f"""
These properties are {key} properties: 
    {newline + ", ".join(results[key])}
"""
            message += msg

    if len(results[CHECKED_PROPERTY_CASES[-1]]) != 0:
        message += f"""
However, We highly suggest you to fix with these properties:

    {newline.join([" - "+text+newline+f"{', '.join(pps)}" for text, pps in results['Failed'].items()])}
        """
    else:
        message += f"""
No big issue with the named properties in general.
        """

    if len(results[CHECKED_PROPERTY_CASES[-2]]) != 0:
        message += f"""
Some warnings related to metadata:

    {newline.join([" - "+text for text in results['Metadata']])}
        """
    else:
        message += f"""
No warning with metadata.        
        """
    return message