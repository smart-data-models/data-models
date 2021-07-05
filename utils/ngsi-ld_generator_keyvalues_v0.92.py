#################################################################################
#  Licensed to the FIWARE Foundation (FF) under one                             #
#  or more contributor license agreements. The FF licenses this file            #
#  to you under the Apache License, Version 2.0 (the "License");                #
#  you may not use this file except in compliance                               #
#  with the License.  You may obtain a copy of the License at                   #
#                                                                               #
#      http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                               #
#  Unless required by applicable law or agreed to in writing, software          #
#  distributed under the License is distributed on an "AS IS" BASIS,            #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     #
#  See the License for the specific language governing permissions and          #
# limitations under the License.                                                #
#################################################################################
# This file generates a payload compliant with NGSI-Ld keyvalues format         #
# input : Schema url in raw format coming from smart data models initiative     #
#################################################################################
import json
import sys
from faker import Faker
fake = Faker()

def extract_datamodel_from_raw_url(schemaUrl):
    # Extract data model name from url
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


def open_jsonref(fileUrl):
    # read json files or url
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


def fake_uri(propertyName, dataModel):
    # generates fake uri
    output = "urn:ngsi-ld:" + str(dataModel) + ":" + str(propertyName) + ":"
    output += fake.bothify(text="????:########", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # genera example uri
    return output


def payload_uri(propertyName, dataModel):
    return {"type": "Property", "value": fake_uri(propertyName, dataModel)}


def payload_relationship(propertyName, dataModel):
    return {"type": "object", "value": fake_uri(propertyName, dataModel)}


def fake_geoproperty(type):
    # generates fake geoproperty
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
    #Generate fake number
    Faker.seed(0)
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
            maximum = 1000
    return fake.pyfloat(left_digits=leftDigits, right_digits=1, min_value=minimum, max_value=maximum)


def fake_integer(*args):
    # generate fake integers
    Faker.seed(0)
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
            maximum = 1000
    return fake.pyint(minimum, maximum)


def payload_number(*args):
    return {"type": "Property", "value": fake_number(*args)}

def payload_interger(*args):
    return {"type": "Property", "value": fake_integer(*args)}


def fake_date():
    # genera example date
    return fake.date(pattern='%Y-%m-%dT%H:%M:%SZ', end_datetime=None)


def payload_date():
    return {"type": "Property", "value" : {"@type": "DateTime", "@value": fake_date()}}


def fake_string(length):
    # genera example string (regular)
    if length == 1:
        return fake.paragraphs(nb=length)[0]
    else:
        return fake.paragraphs(nb=length)


def payload_string(length):
    return {"type": "Property", "value": fake_string(length)}


def fake_enum(elementsList, length):
    # generate fake enumerations
    if length == 1:
        return fake.random_choices(elements=elementsList, length=length)[0]
    else:
        return fake.random_choices(elements=elementsList, length=length)


def payload_enum(elementsList, length):
    return {"type": "Property", "value": fake_enum(elementsList, length)}


def fake_boolean():
    # because False in python starts with capital letter
    return fake.random_choices(elements=["true", "false"], length=1)


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
    if type is not "array" and type is not "object":
        return {"type": "Property", "value": fake_array(type, numItems, options)}
    else:
        return pendingToImplement


def parse_property(fullPayload, dataModel, level):
    # parse a property of the data model
    prop = [p for p in fullPayload.keys()][0]
    # echo("prop", prop)
    payload = fullPayload[prop]
    keys = [k for k in payload]
    # echo("keys", keys)

    if "description" in keys:
        # [description, Property/Relationship/Geoproperty, Model, Units, Enum, Privacy]
        metadata = parse_schema_description(payload["description"])
    else:
        metadata = ["", "Property"]
    if prop == "id" and level == 0:
        return {"id": fake_uri("id", dataModel)}
    elif prop == "id" and level > 0:
        return payload_uri("id", "id")
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
                argsNumber = argsNumber + (1000,)
            return payload_number(argsNumber)
        elif payload["type"] == "integer":
            argsNumber = (4,)
            ### treating number with/without maximum/minimum ###
            if "minimum" in payload:
                argsNumber = argsNumber + (int(payload["minimum"]),)
            else:
                argsNumber = argsNumber + (0,)
            if "maximum" in payload:
                argsNumber = argsNumber + (int(payload["maximum"]),)
            else:
                argsNumber = argsNumber + (1000,)
            return payload_number(argsNumber)
        elif payload["type"] == "string" and "format" in keys:
            if payload["format"] == "date-time":
                return payload_date()
            elif payload["format"] == "uri":
                return payload_uri(prop, dataModel)
        elif payload["type"] == "string" and "enum" in keys:
            return payload_enum(payload["enum"], 1)
        elif payload["type"] == "string":
            return payload_string(1)
        elif payload["type"] == "boolean":
            return payload_boolean()
        elif payload["type"] == "array":
            if "minitems" in payload:
                arrayItems = payload["minitems"]
            else:
                arrayItems = 2
            if "maxitems" in payload:
                arrayItems = int((arrayItems + int(payload["maxitems"]))/2)
            else:
                arrayItems = arrayItems
            valuesArray = [parse_property({"items":payload["items"]}, dataModel, level+1)["value"] for i in range(arrayItems)]
            return {"type": "Property", "value": valuesArray}
        elif payload["type"] == "object":
            valuesObject = {}
            for p in payload["properties"]:
                # echo("{prop: payload[properties]}", {p: payload["properties"][p]})
                valuesObject[p] = parse_property({p: payload["properties"][p]}, dataModel, level+1)["value"]

            return {"type": "Property", "value": valuesObject}
    elif "oneOf" in keys:
        return parse_property({prop: fullPayload[prop]["oneOf"][0]}, dataModel, level)
    else:
        return {prop: pendingToImplement, "value": fake_uri(prop, dataModel)}


schemaUrl = sys.argv[1]
dataModel = extract_datamodel_from_raw_url(schemaUrl)
pendingToImplement = "Version 0.1 not implemented"
missingEntity = "Missing entity name"

#echo("schemaUrl",schemaUrl)
payload = open_jsonref(schemaUrl)
# print(payload["allOf"])
output = {}
fullDict = {}
#echo("payload", payload)
for index in range(len(payload["allOf"])):
    if "properties" in payload["allOf"][index]:
        fullDict = {**fullDict, **payload["allOf"][index]["properties"]}
    else:
        fullDict = {**fullDict, **payload["allOf"][index]}


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
output["@context"] = ["https://smartdatamodels.org/context.jsonld"]
print(json.dumps(output))
