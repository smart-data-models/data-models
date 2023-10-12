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
import os
import json
import random
import string
import sys

from faker import Faker
import requests
import rstr
import ruamel.yaml as yaml


fake = Faker()

pendingToImplement = "Version 0.1 not implemented"
missingEntity = "Missing entity name"


def open_yaml(file_url):
    """
    Opens a YAML file either from a URL or a local file path and returns its content as a dictionary.
    """
    try:
        # Check if the file has a .yaml extension
        _, file_extension = os.path.splitext(file_url)
        if file_extension.lower() != '.yaml':
            raise ValueError("Invalid file format. The file should have a .yaml extension.")
        
        if file_url.startswith("http"):
            # It is a URL
            pointer = requests.get(file_url)
            return yaml.safe_load(pointer.content.decode('utf-8'))
    except:
        return "Exception"
    else:
        # It is a file
        try:
            file = open(file_url, "r")
            return yaml.safe_load(file.read())
        except:
            return "Wrong file path"
        

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
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True)
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