#################################################################################
#  Licensed to the FIWARE Foundation (FF) under one                             #
#  or more contributor license agreements. The FF licenses this file            #
#  to you under the Apache License, Version 2.0 (the "License")                 #
#  you may not use this file except in compliance with the License.             #
#  You may obtain a copy of the License at                                      #
#                                                                               #
#      http://www.apache.org/licenses/LICENSE-2.0                               #
#                                                                               #
#  Unless required by applicable law or agreed to in writing, software          #
#  distributed under the License is distributed on an "AS IS" BASIS,            #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     #
#  See the License for the specific language governing permissions and          #
#  limitations under the License.                                               #
#################################################################################

import sys
import datetime

import jsonschema
import pytz
import json
from validator_collection import checkers
from jsonschema import validate
from pymongo import MongoClient

import yaml


def open_jsonref(fileUrl):
    import jsonref
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=False)
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
    if "oneOf" in schemaPayload:
        # echo("allOf level", level)
        for index in range(len(schemaPayload["oneOf"])):
            # echo("passing to next level this payload=", str(schemaPayload["allOf"][index]))
            partialOutput = parse_payload(schemaPayload["oneOf"][index], level + 1)
            output = dict(output, **partialOutput)
    if "anyOf" in schemaPayload:
        #echo("anyOf level", level)
        for index in range(len(schemaPayload["anyOf"])):
            #echo("original output", output)
            partialOutput = parse_payload(schemaPayload["anyOf"][index], level + 1)
            #echo("parsed anyOf", partialOutput)
            output = dict(output, **partialOutput)
            #echo("current output", output)
    if "properties" in schemaPayload:
        #echo("properties level", level)
        for prop in schemaPayload["properties"]:
            #echo(" dealing at level " + str(level) + " with prop=", prop)
            if "allOf" in prop:
                #echo("original output", output)
                #echo("parsed allOf", partialOutput)
                output[prop] = parse_payload(schemaPayload["properties"]["allOf"], level + 1)
            elif "oneOf" in prop:
                #echo("original output", output)
                #echo("parsed allOf", partialOutput)
                output[prop] = parse_payload(schemaPayload["properties"]["oneOf"], level + 1)
            elif "anyOf" in prop:
                #echo("original output", output)
                #echo("parsed anyOf", partialOutput)
                output[prop] = parse_payload(schemaPayload["properties"]["anyOf"], level + 1)
            else:
                #echo("parsing this payload at " + str(level) + " from prop =" + prop, schemaPayload["properties"][prop])
                try:
                    output[prop]
                except:
                    output[prop] = {}
                for item in list(schemaPayload["properties"][prop]):
                    #echo("parsing at level " + str(level) + " item= ", item)

                    if item == "description":
                        # print("Detectada la descripcion de la propiedad=" + prop)
                        separatedDescription = schemaPayload["properties"][prop]["description"].split(". ")
                        descriptionPieces = []
                        while separatedDescription:
                            descriptionPiece = separatedDescription.pop()
                            if descriptionPiece in propertyTypes:
                                output[prop]["type"] = descriptionPiece
                            elif descriptionPiece.find("Model:") > -1:
                                try:
                                    output[prop]["x-ngsi"]["model"] = descriptionPiece.replace("'", "").replace("Model:", "")
                                except:
                                    output[prop]["x-ngsi"] = {}
                                    output[prop]["x-ngsi"]["model"] = descriptionPiece.replace("'", "").replace("Model:", "")
                            elif descriptionPiece.find("Units:") > -1:
                                try:
                                    output[prop]["x-ngsi"]["units"] = descriptionPiece.replace("'", "").replace("Units:", "")
                                except:
                                    output[prop]["x-ngsi"] = {}
                                    output[prop]["x-ngsi"]["units"] = descriptionPiece.replace("'", "").replace("Units:", "")
                            else:
                                descriptionPieces.append(descriptionPiece)
                        #print("---")
                        description = ". ".join(descriptionPieces)
                        output[prop]["description"] = description  # the remaining part of the description is used

                    elif item == "type":
                        output[prop]["type"] = schemaPayload["properties"][prop]["type"]
                    else:
                        #echo("parsing prop", prop)
                        #echo("payload", schemaPayload["properties"][prop][item])
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

# tests allowed
validTests = {"1": "Check that properties are properly documented"}


# recover call parameters
schemaUrl = sys.argv[1]
mail = sys.argv[2]
test = sys.argv[3]
if len(sys.argv) > 4:
    yamlOutput = sys.argv[4]
    #print(yamlOutput)
else:
    yamlOutput = 0

# validate inputs
existsSchema = exist_page(schemaUrl)

# url provided is an existing url
if not existsSchema[0]:
    output["result"] = False
    output["cause"] = "Cannot find the schema at " + schemaUrl
    output["time"] = str(datetime.datetime.now(tz=tz))
    print(json.dumps(output))
    sys.exit()

# url is actually a json
try:
    schemaDict = json.loads(existsSchema[1])
except ValueError:
    output["result"] = False
    output["cause"] = "Schema " + schemaUrl + " is not a valid json"
    output["time"] = str(datetime.datetime.now(tz=tz))
    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
    print(json.dumps(output))
    sys.exit()

# mail is a real email
if not checkers.is_email(mail):
    output["result"] = False
    output["cause"] = "mail " + schemaUrl + " is not a valid email"
    output["time"] = str(datetime.datetime.now(tz=tz))
    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
    print(json.dumps(output))
    sys.exit()

# check that this test is in the portfolio of tests 8see validTests variable at initialize section
if test not in validTests:
    output["result"] = False
    output["cause"] = "Test does not exist"
    output["time"] = str(datetime.datetime.now(tz=tz))
    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
    output["validTests"] = validTests
    print(json.dumps(output))
    sys.exit()

# test that it is a valid schema against the metaschema
try:
    schema = open_jsonref(schemaUrl)
    # echo("len of schema", len(str(schema)))
    # echo("schema", schema)
    if not bool(schema):
        output["result"] = False
        output["cause"] = "json schema returned empty (wrong $ref?)"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
        output["validTests"] = validTests
        print(json.dumps(output))
        sys.exit()

except:
    output["result"] = False
    output["cause"] = "json schema cannot be fully loaded"
    output["time"] = str(datetime.datetime.now(tz=tz))
    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
    output["validTests"] = validTests
    print(json.dumps(output))
    sys.exit()

try:
    validate(instance=schema, schema=metaSchema)
except jsonschema.exceptions.ValidationError as err:
    # print(err)
    output["result"] = False
    output["cause"] = "schema does not validate as a json schema"
    output["time"] = str(datetime.datetime.now(tz=tz))
    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
    output["errorSchema"] = str(err)
    print(json.dumps(output))
    sys.exit()

# extract properties' definitions
# check if they are populated
if test == "1":  # check that the schema has properly documented the properties
    documented = "documentationStatusOfProperties"
    try:
        yamlDict = parse_payload(schema, 1)
    except:
        output["result"] = False
        output["cause"] = "schema cannot be loaded (possibly invalid $ref)"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
        print(json.dumps(output))
        sys.exit()
    # echo("yamlDict", yamlDict)
    output[documented] = {}
    for key in yamlDict:
        # print(key)
        # print(yamlDict[key])
        ################### warning ###################
        # this will fail wit any attribute defined through a oneOf, allOf or anyOf
        ################### warning ###################

        if key != "id":  # this will
            try:
                propertyType = yamlDict[key]["type"]
                if propertyType in propertyTypes:
                    # print(propertyType)
                    # print(propertyTypes)
                    output[documented][key] = {}
                    output[documented][key]["x-ngsi"] = True
                    output[documented][key]["x-ngsi_text"] = "ok to " + str(propertyType)
                else:
                    output[documented][key]["x-ngsi"] = False
                    output[documented][key]["x-ngsi_text"] = "Wrong NGSI type of " + propertyType + " in the description of the property"
            except:
                output[documented][key] = {}
                output[documented][key]["x-ngsi"] = False
                output[documented][key]["x-ngsi_text"] = "Missing NGSI type of " + str(propertyTypes) + " in the description of the property"

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


    output["schemaDiagnose"] = "This schema has " + str(allProperties) + " properties. " + str(notDescribedProperties) +" properties are not described at all and " + str(faultyDescriptionProperties) + " have descriptions that must be completed. " + str(allProperties - faultyDescriptionProperties - notDescribedProperties) + " are described but you can review them anyway. "

# now it checks if these properties already exist in the database
try:
    mongoDb = "smartdatamodels"
    mongoCollection = "properties"
    host = "localhost"
    db_user = "db_user"
    password = "F1w4re--"
    database = "datamodels"
    client = MongoClient()
    db = client[mongoDb]
    collProperties = db[mongoCollection]
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
        patternKey = "^"+ lowKey + "$"
        queryKey = {"property": {"$regex": patternKey, "$options": "i"}}

        results = list(collProperties.find(queryKey))
        #print(len(results))
        if len(results) > 0:
            definitions= []
            dataModelsList = []
            types = []
            for index, item in enumerate(results):
                definitions.append(str(index + 1) + ".-" + item["description"])
                dataModelsList.append(str(index + 1) + ".-" + item["dataModel"])
                #print(item["type"])
                types.append(str(index + 1) + ".-" +  item["type"])
            output[existing].append({key: "Already used in data models: " + ",".join(dataModelsList) + " with these definitions: " + chr(13).join(definitions) + " and these data types: " + ",".join(types)})
        else:
            output[available].append({key: "Available"})

except:
    output[existing].append({"Error": lowKey})

# check that the header derivedFrom attributes are properly reported
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
                if not exist_page(derivedFrom)[0]:
                    output["metadata"]["derivedFrom"] = {"warning": "derivedFrom url is not reachable"}
    else:
        output["metadata"]["derivedFrom"] = {"warning": "not derivedFrom clause, include derivedFrom = '' in the header"}
except:
    output["metadata"]["derivedFrom"] = {"warning": "not possible to check derivedFrom clause, Does it exist a derivedFrom = '' clause in the header?"}

# check that the title exist
try:
    metadata = "metadata"
    if "metadata" not in output:
        output[metadata] = {}
    if "title" in schemaDict:
        title = schemaDict["title"]
        if title == "":
            output["metadata"]["title"] = {"warning": "Title is empty"}
        elif not isinstance(title, str):
            output["metadata"]["title"] = {"warning": "Title is not a string"}
        elif len(title) < 15:
            output["metadata"]["title"] = {"warning": "Title too short"}
    else:
        output["metadata"]["title"] = {"warning": "Missing title clause, , include title = '' in the header"}
except:
    output["metadata"]["title"] = {"warning": "not possible to check title clause, Does it exist a title = '' in the header?"}

# check that the description  exists
try:
    metadata = "metadata"
    if "metadata" not in output:
        output[metadata] = {}
    if "description" in schemaDict:
        description = schemaDict["description"]
        if description == "":
            output["metadata"]["description"] = {"warning": "Description is empty"}
        elif not isinstance(description, str):
            output["metadata"]["description"] = {"warning": "Description is not a string"}
        elif len(title) < 34:
            output["metadata"]["description"] = {"warning": "Description is too short"}
    else:
        output["metadata"]["description"] = {"warning": "Missing description clause, include description = '' in the header"}
except:
    output["metadata"]["description"] = {"warning": "not possible to check description clause, does it exist a description = '' in the header?"}

# check that the tags  exist
try:
    metadata = "metadata"
    if "metadata" not in output:
        output[metadata] = {}
    if "modelTags" in schemaDict:
        modelTags = schemaDict["modelTags"]
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
    if "$schemaVersion" in schemaDict:
        schemaVersion = schemaDict["$schemaVersion"]
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
                if not exist_page(license)[0]:
                    output["metadata"]["license"] = {"warning": "license url is not reachable"}
        else:
            output["metadata"]["license"] = {"warning": "license is empty, include a license = '' in the header "}
    else:
        output["metadata"]["license"] = {"warning": "not license clause, does it exist a license = '' in the header?"}
except:
    output["metadata"]["license"] = {"warning": "not possible to check license clause"}

# check that the required clause exists
try:
    metadata = "metadata"
    if "metadata" not in output:
        output[metadata] = {}
    if "required" in schemaDict:
        required = schemaDict["required"]
        print(required)
        print(type(required))
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


if yamlOutput == "1":
    print(yaml.safe_dump(output, default_flow_style=False))
else:
    print(json.dumps(output))


