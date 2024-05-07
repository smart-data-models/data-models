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
import re

import string
import jsonref
from typing import Dict, Tuple

from validator_collection import checkers


from faker import Faker
import requests
import rstr
import ruamel.yaml


fake = Faker()

pendingToImplement = "Version 0.1 not implemented"
missingEntity = "Missing entity name"

newline = "\n  "
newsubline = "\n   "
propertyTypes = ["Property", "Relationship", "GeoProperty"]

# property check
incompleteDescription = "Incomplete description"
withoutDescription = "No description at all"
wrongTypeDescription = "Wrong NGSI types"
missingTypeDescription = "Missing NGSI types"
exceptions = ["coordinates", "bbox", "type"]

KEYWORDS_FOR_CERTAIN_CHECK = "smart-data-models"
CHECKED_PROPERTY_CASES = ['well documented', 'already used', 'newly available', 'Metadata', 'Failed']

# Regular expression pattern to extract owner, repository, branch, and file path
github_url_pattern = r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)"

def is_url_existed(url):
    """
        Check if a URL exists and retrieve its content.
        Parameters:
        - url (str): The URL to check.
        Returns:
        - list[bool, str]: A list containing a boolean indicating if the URL exists,
          and either the content of the URL if it exists, or the HTTP status code
          if it doesn't. If there's an exception during the request, it returns
          a boolean indicating failure and an error message.
        Example:
            is_url_existed("https://example.com")
        [True, 'Content of the URL']
            is_url_existed("https://nonexistent-url.com")
        [False, 404]
            is_url_existed("invalid-url")
        [False, 'wrong domain']
        """

    try:
        pointer = requests.get(url)
        if pointer.status_code == 200:
            return [True, pointer.text]
        else:
            return [False, pointer.status_code]
    except:
        return [False, "wrong domain"]


def open_json(fileUrl: str):
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    >>> open_json("https://example.com/data.json")
    {...}
    >>> open_json("local_file.json")
    {...}
    >>> open_json("invalid-url")
    None
    """
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


def open_jsonref(fileUrl: str):
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Capable of parsing JSON file with $ref
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    >>> open_jsonref("https://example.com/data.json")
    {...}
    >>> open_jsonref("local_file.json")
    {...}
    >>> open_jsonref("invalid-url")
    None
    """
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True, merge_props=True)
            return output
        except:
            return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read(), load_on_repr=True, merge_props=True)
        except:
            return None


def open_yaml(file_url):
    """
    Opens a YAML file either from a URL or a local file path and returns its content as a dictionary.
    """
    yaml = ruamel.yaml.YAML(typ='safe')
    try:
        _, file_extension = os.path.splitext(file_url)
        if file_extension.lower() != '.yaml':
            print("Invalid file format. The file should have a .yaml extension.")

        if file_url.startswith("http"):
            if re.match(github_url_pattern, file_url):
                raw_github_url = convert_to_raw_github_url(file_url)
                response = requests.get(raw_github_url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return yaml.load(response.content.decode('utf-8'))
            else:
                response = requests.get(file_url)
                response.raise_for_status()
                return yaml.load(response.content.decode('utf-8'))
        else:
            with open(file_url, "r") as file:
                return yaml.load(file)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch content from URL: {e}")
    except Exception as e:
        print(f"Error: {e}")
        

def extract_datamodel_from_raw_url(schemaUrl: str) -> str:
    """
    Extracts the name of the data model from the given schema repository URL.
    Parameters:
    - schema_url (str): The URL of the schema repository.
    Returns:
    - str: The name of the data model extracted from the URL. Return 'dataModel' as a flag naming doesn't find any match
    Example:
    >>> extract_datamodel_from_raw_url("https://raw.githubusercontent.com/smart-data-models/dataModel.WasteWater/master/WaterProcess/schema.json")
    'WaterProcess'
    >>> extract_datamodel_from_raw_url("https://smart-data-models.github.io/dataModel.WasteWater/WaterProcess/schema.json")
    'WaterProcess'
    >>> extract_datamodel_from_raw_url("invalid-url")
    'dataModel'
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

def extract_subject_from_raw_url(schemaUrl: str) -> str:
    """
    Extracts the name of the subject from the given schema repository URL.
    Parameters:
    - schema_url (str): The URL of the schema repository.
    Returns:
    - str: The name of the subject extracted from the URL. Return 'subject' as a flag naming doesn't find any match
    Example:
    >>> extract_datamodel_from_raw_url("https://raw.githubusercontent.com/smart-data-models/dataModel.WasteWater/master/WaterProcess/schema.json")
    'dataModel.WasteWater'
    >>> extract_datamodel_from_raw_url("https://smart-data-models.github.io/dataModel.WasteWater/WaterProcess/schema.json")
    'dataModel.WasteWater'
    >>> extract_datamodel_from_raw_url("invalid-url")
    'subject'
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


def create_context(subject: str) -> str:
    """
    Creates the link to context.jsonld of given subject

    Parameters:
    - subject (str): The name of the subject.

    Returns:
    - str: The link of the context.jsonld

    Example:
    >>> create_context("dataModel.WasteWater")
    'https://smart-data-models.github.io/dataModel.WasteWater/context.jsonld'
    """
    return "https://smart-data-models.github.io/" + subject + "/context.jsonld"

#########################################
#   Conversion between different examples
#########################################

@DeprecationWarning
def normalized2keyvalues(normalizedPayload: dict) -> dict:
    """
    Converts the normalized format example to key-value format example
    Parameters:
    - normalizedPayload (str): The JSON payload of the normalized format example.
    Returns:
    - dict: The JSON payload of the key-value format example
    Example:
       normalized2keyvalues(
        {
            "id": "urn:waterdna:haemil:WaterProcess_01",
            "type": "WaterProcess",
            "location": {
                "type": "geo:json",
                "value": {
                    "type": "Point",
                    "coordinates": [
                            127.266663,
                            36.524677
                        ]
                    }
            },
            "name": {
                "type": "Text",
                "value": "inflow process at water treatment plant 1"
            },
            ...
        }
    )
    {
        "id": "urn:waterdna:haemil:WaterProcess_01",
        "type": "WaterProcess",
        "location": {
            "type": "Point",
            "coordinates": [
                    127.266663,
                    36.524677
                ]
        },
        "name": "inflow process at water treatment plant 1",
        ...
    }
    """

    normalizedDict = normalizedPayload
    output = {}

    for element in normalizedDict:
        try:
            # In a normalized format, `type` and `value` are two mandatory keys
            # To get the key-value format, simply by taking the value inside `value`
            if "value" in normalizedDict[element]:
                value = normalizedDict[element]["value"]
                # In NGSI-LD normalized format, `@type` and `@value` are used to represent
                # DateTime as a sub-structure inside `value`
                # If `@type` exists, then take the value inside `@value`
                if "@type" in value:
                    output[element] = normalizedDict[element]["value"]["@value"]
                else:
                    output[element] = value
            else:
                output[element] = normalizedDict[element]
        except:
            output[element] = normalizedDict[element]

    return output

def normalized2keyvalues_v2(normalizedPayload: dict, level: int = 0) -> dict:
    """
    Converts the normalized format example to key-value format example, version 2
    Could be applied to normalized.json or normalized.jsonld

    Parameters:
    - normalizedPayload (str): The JSON payload of the normalized format example.

    Returns:
    - dict: The JSON payload of the key-value format example
    """
    output = {}
    for element, body in normalizedPayload.items():

        # If the body is a list of dictionary
        # recursively process the list, get the sub-structure of `value` if it exists
        if isinstance(body, list) and body and isinstance(body[0], dict):
            output[element] = [normalized2keyvalues_v2(subprop, level + 1).get("value", subprop) for subprop in body]

        # If the body is a dictionary, then process it in detail
        elif isinstance(body, dict):

            # Get the sub-structure of `@value` if it exists
            # This refers to the case of DateTime in NGSI-LD
            # Example: {"type": "Property", "value": {"@type": "DateTime", "@value": "xxx"}}
            if "@value" in body:
                output[element] = body["@value"]

            elif "value" in body:
                value = body["value"]

                # If the value is a dictionary, then recursively process the value
                if isinstance(value, dict):
                    output[element] = normalized2keyvalues_v2({"value": value}, level + 1)["value"]

                # If the value is a list of dictionary
                # then recursively process the list, get the sub-structure of `value` if it exists
                elif isinstance(value, list) and value and isinstance(value[0], dict):
                    output[element] = [normalized2keyvalues_v2(subvalue, level + 1).get("value", subvalue) for subvalue
                                       in value]

                # Otherwise, use the value as is
                else:
                    output[element] = value

            # Get the sub-structure of `object` if it exists
            # This refers to the case of Relationship in NGSI-LD
            # Example: {"type": "Relationship", "object": "xxxx"}
            elif "object" in body:
                output[element] = body["object"]

            # Otherwise, use the body as is
            else:
                output[element] = body

        # Otherwise, use the body as is
        else:
            output[element] = body

    return output

def keyvalues2normalized_ngsild(keyvaluesPayload: dict, yamlDict: dict, detailed: bool = True, level: int = 0) -> dict:
    """
    Converts the key-value format example to normalized format example in NGSI-LD

    Parameters:
    - keyvaluesPayload (dict): The JSON payload of the key-value format example.
    - yamlDict (dict): The schema dictionary.
    - detailed (bool): Whether generate only the first-level properties or for all in detailed
    - level (int): Level of recursion.

    Returns:
    - dict: The JSON payload of the normalized.jsonld format example
    """
    import json

    def valid_date(datestring: str) -> tuple[bool, str]:
        """
        Valid the date string and return the specific type according to the patterns, "Date", "DateTime", "Time", "Text"
        """
        import re
        from datetime import time

        if not ("T" in datestring) and ("Z" in datestring):
            try:
                time.fromisoformat(datestring.replace('Z', '+00:00'))
            except:
                return False, "Text"
            return True, "Time"

        else:
            date = datestring.split("T")[0]
            try:
                validDate = re.match('^[0-9]{2,4}[-/][0-9]{2}[-/][0-9]{2,4}$', date)
            except ValueError:
                return False, "Text"

            if validDate is not None:
                if len(datestring.split("T")) > 1:
                    return True, "DateTime"
                return True, "Date"
            else:
                return False, "Text"

    keyvaluesDict = keyvaluesPayload
    output = {}
    for element in keyvaluesDict:

        # id, type, @context, are in key-value format by default
        if level == 0 and element in ["id", "type", "@context"]: continue
        item = {}

        if isinstance(keyvaluesDict[element], list):
            # it is an array
            item["type"] = yamlDict[element]['x-ngsi']['type']
            if detailed:
                if len(keyvaluesDict[element]) > 0 and isinstance(keyvaluesDict[element][0], dict):
                    tmpList = []
                    for idx in range(len(keyvaluesDict[element])):
                        tmpList.append(keyvalues2normalized_ngsild(keyvaluesDict[element][idx], yamlDict[element][idx],
                                                                   level=level + 1))
                    item["value"] = tmpList
                else:
                    item["value"] = keyvaluesDict[element]
            else:
                item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], dict):
            # it is an object
            # item["type"] = "object"
            if element == "location":
                item["type"] = yamlDict[element]['x-ngsi']['type']
            elif "type" in keyvaluesDict[element] and "coordinates" in keyvaluesDict[element]:  # location-like property
                item["type"] = yamlDict[element]['x-ngsi']['type']
            else:
                item["type"] = yamlDict[element]['x-ngsi']['type']
            if detailed:
                item["value"] = keyvalues2normalized_ngsild(keyvaluesDict[element], yamlDict[element], level=level + 1)
            else:
                item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], str):
            dateFlag, dateType = valid_date(keyvaluesDict[element])
            if dateFlag:
                # it is a date
                item["type"] = yamlDict[element]['x-ngsi']['type']
                if dateType == "Date":
                    item["value"] = {"@type": "Date", "@value": keyvaluesDict[element]}
                elif dateType == "Time":
                    item["value"] = {"@type": "Time", "@value": keyvaluesDict[element]}
                else:
                    item["value"] = {"@type": "DateTime", "@value": keyvaluesDict[element]}
            else:
                # it is a string
                item["type"] = yamlDict[element]['x-ngsi']['type']
                item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], int) or isinstance(keyvaluesDict[element], float):
            # it is a number
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = keyvaluesDict[element]

        elif keyvaluesDict[element] == True:
            # it is a boolean for true
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = json.loads("true")

        elif keyvaluesDict[element] == False:
            # it is a boolean for false
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = json.loads("false")

        else:
            print("*** other type ***")
            print("I do not know what is it")
            print(keyvaluesDict[element])
            print("--- other type ---")
        output[element] = item

    if "id" in keyvaluesDict:
        output["id"] = keyvaluesDict["id"]
    if "type" in keyvaluesDict:
        output["type"] = keyvaluesDict["type"]
    if "@context" in keyvaluesDict:
        output["@context"] = keyvaluesDict["@context"]

    return output

def keyvalues2normalized_ngsiv2(keyvaluesPayload, detailed=True):
    """
    Converts the key-value format example to normalized format example in NGSI-V2

    Parameters:
    - keyvaluesPayload (dict): The JSON payload of the key-value format example.
    - detailed (bool): Whether generate only the first-level properties or for all in detailed

    Returns:
    - dict: The JSON payload of the normalized.json format example
    """
    import json

    def valid_date(datestring: str) -> bool:
        """
        Valid the date string and return the specific type according to the patterns, "DateTime", "Text", only two types in NGSI-V2
        """
        import re
        date = datestring.split("T")[0]
        try:
            validDate = re.match('^[0-9]{2,4}[-/][0-9]{2}[-/][0-9]{2,4}$', date)
        except ValueError:
            return False

        if validDate is not None:
            return True
        else:
            return False

    keyvaluesDict = keyvaluesPayload
    output = {}

    for element in keyvaluesDict:
        item = {}

        if isinstance(keyvaluesDict[element], list):
            # it is an array
            # item["type"] = "array"
            item["type"] = "StructuredValue"
            if detailed:
                if len(keyvaluesDict[element]) > 0 and isinstance(keyvaluesDict[element][0], dict):
                    tmpList = []
                    for idx in range(len(keyvaluesDict[element])):
                        tmpList.append(keyvalues2normalized_ngsiv2(keyvaluesDict[element][idx]))
                    item["value"] = tmpList
                else:
                    item["value"] = keyvaluesDict[element]
            else:
                item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], dict):
            # it is an object
            if element == "location":
                item["type"] = "geo:json"
            else:
                item["type"] = "StructuredValue"
            if detailed:
                item["value"] = keyvalues2normalized_ngsiv2(keyvaluesDict[element])
            else:
                item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], str):
            if valid_date(keyvaluesDict[element]):
                # it is a date
                item["type"] = "DateTime"
            else:
                # it is a string
                item["type"] = "Text"
            item["value"] = keyvaluesDict[element]

        elif isinstance(keyvaluesDict[element], int) or isinstance(keyvaluesDict[element], float):
            # it is a number
            item["type"] = "Number"
            item["value"] = keyvaluesDict[element]

        elif keyvaluesDict[element] == True:
            # it is a boolean
            item["type"] = "Boolean"
            item["value"] = json.loads("true")

        elif keyvaluesDict[element] == False:
            # it is a boolean
            item["type"] = "Boolean"
            item["value"] = json.loads("false")

        else:
            print("*** other type ***")
            print("I do now know what is it")
            print(keyvaluesDict[element])
            print("--- other type ---")
        output[element] = item

    if "id" in output:
        output["id"] = output["id"]["value"]
    if "type" in output:
        output["type"] = output["type"]["value"]
    if "@context" in output:
        output["@context"] = output["@context"]["value"]

    return output

def generate_random_string(length=4) -> str:
    """
    Generates a random string of the specified length.
    Parameters:
    - length (int): The length of the random string. Default is 4.
    Returns:
    - str: The generated random string.
    Example:
    >>> generate_random_string()
    'aB3x'
    >>> generate_random_string(8)
    'y2RtL6zA'
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

########################################
#   Generate fake example related
########################################

def fake_uri(propertyName:str, dataModel:str) -> str:
    """
        Generates a fake URI based on the provided property name and data model.
        Parameters:
        - propertyName (str): The name of the property.
        - dataModel (str): The name of the data model.
        Returns:
        - str: The generated fake URI.
        Example:
        >>> fake_uri("temperature", "WeatherObserved")
        'urn:ngsi-ld:WeatherObserved:temperature:ABCD1234'
        """
    output = "urn:ngsi-ld:" + str(dataModel) + ":" + str(propertyName) + ":"
    output += fake.bothify(text="????:########", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # genera example uri
    return output

def payload_uri(propertyName: str, dataModel: str) -> dict:
    """
       Generates a payload containing a URI value for a Property.
       Parameters:
       - propertyName (str): The name of the property.
       - dataModel (str): The name of the data model.
       Returns:
       - dict: A payload containing a URI value.
       Example:
       >>> payload_uri("temperature", "WeatherObserved")
       {'type': 'Property', 'value': 'urn:ngsi-ld:WeatherObserved:temperature:ABCD1234'}
       """
    return {"type": "Property", "value": fake_uri(propertyName, dataModel)}

def payload_relationship(propertyName, dataModel):
    """
        Generates a payload containing a URI value for a Relationship.
        Parameters:
        - propertyName (str): The name of the relationship property.
        - dataModel (str): The name of the data model.
        Returns:
        - dict: A payload containing a relationship property.
        Example:
        >>> payload_relationship("belongsTo", "Building")
        {'type': 'Relationship', 'object': 'urn:ngsi-ld:Building:belongsTo:ABCD1234'}
        TODO
        Copy with different data structure relationships, like list and dict
        """
    return {"type": "object", "value": fake_uri(propertyName, dataModel)}


def fake_geoproperty(geo_type: str) -> dict:
    """
    Generates a fake GeoJSON property based on the given geometry type.

    Parameters:
    - geo_type (str): The type of the geometry (e.g., "Point", "LineString", "Polygon").

    Returns:
    - dict: A GeoJSON property with fake coordinates.

    Example:
    >>> fake_geoproperty("Point")
    {'type': 'Point', 'coordinates': [12.345, -67.890]}

    TODO
    To support more geo_types
    """
    dict_value = {}

    if geo_type == "Point":
        dict_value = {"type": geo_type, "coordinates": [float(fake.latitude()), float(fake.longitude())]}
    elif geo_type == "LineString":
        dict_value = {"type": geo_type, "coordinates": [
            [float(fake.latitude()), float(fake.longitude())],
            [float(fake.latitude()), float(fake.longitude())]
        ]}
    elif geo_type == "Polygon":
        dict_value = {"type": geo_type, "coordinates": [
            [float(fake.latitude()), float(fake.longitude())],
            [float(fake.latitude()), float(fake.longitude())],
            [float(fake.latitude()), float(fake.longitude())],
            [float(fake.latitude()), float(fake.longitude())]
        ]}

    return dict_value

def payload_geoproperty(geo_type: str) -> dict:
    """
    Generates a GeoJSON property payload with a fake geometry based on the given type.

    Parameters:
    - geo_type (str): The type of the geometry (e.g., "Point", "LineString", "Polygon").

    Returns:
    - dict: A GeoJSON property payload.

    Example:
    >>> payload_geoproperty("Point")
    {'type': 'GeoProperty', 'value': {'type': 'Point', 'coordinates': [12.345, -67.890]}}
    """
    return {"type": "GeoProperty", "value": fake_geoproperty(geo_type)}


def fake_number(*args) -> float:
    """
    Generates a fake floating-point number based on the provided arguments.

    Parameters:
    - If only one argument is provided (an integer), it represents the number of left digits (default is 6).
    - If more than one argument is provided as a tuple, the first element is the number of left digits (default is 6),
      the second element is the minimum value (default is 0), and the third element is the maximum value
      (default is maximum of 1000 or minimum + 1000).

    Returns:
    - float: A fake floating-point number.

    Example:
    >>> fake_number()
    123.4

    >>> fake_number(8)
    12345678.9

    >>> fake_number((8, 100, 500))
    123456.7
    """
    Faker.seed()

    if isinstance(args[0], int):
        left_digits = 6
        minimum = 0
        maximum = 1000
    else:
        left_digits = int(args[0][0])
        minimum = int(args[0][1]) if len(args[0]) > 1 else 0
        maximum = int(args[0][2]) if len(args[0]) > 2 else max(1000, minimum + 1000)

    return fake.pyfloat(left_digits=left_digits, right_digits=1, min_value=minimum, max_value=maximum)

def fake_integer(*args) -> int:
    """
    Generates a fake integer based on the provided arguments.

    Parameters:
    - If only one argument is provided (an integer), it represents the maximum value (default is 1000).
    - If more than one argument is provided as a tuple, the first element is the minimum value (default is 0),
      and the second element is the maximum value (default is maximum of 1000 or minimum + 1000).

    Returns:
    - int: A fake integer.

    Example:
    >>> fake_integer()
    42

    >>> fake_integer(50)
    25

    >>> fake_integer((10, 50))
    37
    """
    Faker.seed()

    if isinstance(args[0], int):
        minimum = 0
        maximum = args[0]
    else:
        minimum = int(args[0][0]) if len(args[0]) > 0 else 0
        maximum = int(args[0][1]) if len(args[0]) > 1 else max(1000, minimum + 1000)

    return fake.pyint(minimum, maximum)

def payload_number(*args) -> dict:
    """
    Generates a payload for a fake number property based on the provided arguments.

    Parameters:
    - If only one argument is provided (an integer), it represents the maximum value (default is 1000).
    - If more than one argument is provided as a tuple, the first element is the number of left digits (default is 6),
      the second element is the minimum value (default is 0), and the third element is the maximum value
      (default is maximum of 1000 or minimum + 1000).

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake number value.

    Example:
    >>> payload_number()
    {'type': 'Property', 'value': 42.3}

    >>> payload_number(50)
    {'type': 'Property', 'value': 25.7}

    >>> payload_number((6, 10, 50))
    {'type': 'Property', 'value': 37.9}
    """
    return {"type": "Property", "value": fake_number(*args)}

def payload_integer(*args) -> dict:
    """
    Generates a payload for a fake integer property based on the provided arguments.

    Parameters:
    - If only one argument is provided (an integer), it represents the maximum value (default is 1000).
    - If more than one argument is provided as a tuple, the first element is the minimum value (default is 0),
      and the second element is the maximum value (default is maximum of 1000 or minimum + 1000).

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake integer value.

    Example:
    >>> payload_integer()
    {'type': 'Property', 'value': 42}

    >>> payload_integer((10, 50))
    {'type': 'Property', 'value': 37}
    """
    return {"type": "Property", "value": fake_integer(*args)}

def fake_datetime() -> str:
    """
    Generates a fake datetime string in the format '%Y-%m-%dT%H:%M:%SZ'.

    Returns:
    - str: A fake datetime string.

    Example:
    >>> fake_datetime()
    '2023-05-16T14:23:45Z'
    """
    return fake.date(pattern='%Y-%m-%dT%H:%M:%SZ', end_datetime=None)


def fake_date() -> str:
    """
    Generates a fake date string in the format '%Y-%m-%d'.

    Returns:
    - str: A fake date string.

    Example:
    >>> fake_date()
    '2023-05-16'
    """
    return fake.date(pattern='%Y-%m-%d', end_datetime=None)

def fake_time() -> str:
    """
    Generates a fake time string in the format '%H:%M:%SZ'.

    Returns:
    - str: A fake time string.

    Example:
    >>> fake_time()
    '14:23:45Z'
    """
    return fake.date(pattern='%H:%M:%SZ', end_datetime=None)

def payload_datetime() -> dict:
    """
    Generates a payload for a fake datetime property.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake datetime value.

    Example:
    >>> payload_datetime()
    {'type': 'Property', 'value': {'@type': 'DateTime', '@value': '2023-05-16T14:23:45Z'}}
    """
    return {"type": "Property", "value": {"@type": "DateTime", "@value": fake_datetime()}}

def payload_date() -> dict:
    """
    Generates a payload for a fake date property.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake date value.

    Example:
    >>> payload_date()
    {'type': 'Property', 'value': {'@type': 'Date', '@value': '2023-05-16'}}
    """
    return {"type": "Property", "value": {"@type": "Date", "@value": fake_date()}}

def payload_time() -> dict:
    """
    Generates a payload for a fake time property.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake time value.

    Example:
    >>> payload_time()
    {'type': 'Property', 'value': {'@type': 'Time', '@value': '14:23:45Z'}}
    """
    return {"type": "Property", "value": {"@type": "Time", "@value": fake_time()}}

def fake_email(dataModel: str) -> str:
    """
    Generates a fake email address based on the data model.

    Parameters:
    - dataModel (str): The data model to incorporate into the email address.

    Returns:
    - str: A fake email address.

    Example:
    >>> fake_email('SmartCity')
    'john.doe@smartcity.com'
    """
    list_of_domains = (
        'com',
        'net',
        'org',
        'gov'
    )

    dns_org = fake.random_choices(
        elements=list_of_domains,
        length=1
    )[0]

    return f"{fake.first_name()}.{fake.last_name()}@{dataModel}.{dns_org}".lower()

def payload_email(dataModel: str) -> dict:
    """
    Generates a payload for a fake email property.

    Parameters:
    - dataModel (str): The data model to incorporate into the email address.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake email value.

    Example:
    >>> payload_email('SmartCity')
    {'type': 'Property', 'value': 'john.doe@smartcity.com'}
    """
    return {"type": "Property", "value": fake_email(dataModel)}


def fake_string(length: int, min_length: int, max_length:int) -> str:
    """
    Generate a fake string based on specified length and range.

    Parameters:
    - length (int): Desired length of the string.
    - min_length (int): Minimum possible length of the string.
    - max_length (int): Maximum possible length of the string.

    Returns:
    - str: Fake string.

    Example:
    >>> fake_string(1, 5, 10)
    'Lorem ipsum'
    """
    paragraph_length = random.randint(min_length, max_length)

    # generate example string (regular)
    if length == 1:
        return fake.paragraphs(nb=length)[0][:paragraph_length]
    else:
        return fake.paragraphs(nb=length)

def payload_string(length: int, min_length: int, max_length: int, pattern: str="") -> dict:
    """
    Generate a payload for a string property with optional pattern.

    Parameters:
    - length (int): Desired length of the string.
    - min_length (int): Minimum possible length of the string.
    - max_length (int): Maximum possible length of the string.
    - pattern (str, optional): Regular expression pattern to match.

    Returns:
    - dict: Property payload.

    Example:
    >>> payload_string(1, 5, 10)
    {'type': 'Property', 'value': 'Lorem ipsum'}
    """
    if pattern:
        return {"type": "Property", "value": rstr.xeger(pattern)}
    else:
        return {"type": "Property", "value": fake_string(length, min_length, max_length)}


def fake_enum(elements_list: list, length: int) -> str:
    """
    Generates a fake enum.

    Parameters:
    - elements_list (list): The list of possible enum values.
    - length (int): The number of enum values to generate.

    Returns:
    - str: A fake enum value or a list of fake enum values.

    Example:
    >>> fake_enum(['red', 'blue', 'green'], 1)
    'red'
    """
    if length == 1:
        return fake.random_choices(elements=elements_list, length=length)[0]
    else:
        return fake.random_choices(elements=elements_list, length=length)

def payload_enum(elements_list: list, length: int) -> dict:
    """
    Generates a payload for a fake enum property.

    Parameters:
    - elements_list (list): The list of possible enum values.
    - length (int): The number of enum values to generate.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake enum value or values.

    Example:
    >>> payload_enum(['red', 'blue', 'green'], 3)
    {'type': 'Property', 'value': ['red', 'blue', 'green']}
    """
    return {"type": "Property", "value": fake_enum(elements_list, length)}


def fake_boolean() -> bool:
    """
    Generates a fake boolean value.

    Returns:
    - bool: A random boolean value.

    Example:
    >>> fake_boolean()
    True
    """
    return fake.random_choices(elements=[True, False], length=1)[0]

def payload_boolean() -> dict:
    """
    Generates a payload for a fake boolean property.

    Returns:
    - dict: A payload dictionary with the type 'Property' and a fake boolean value.

    Example:
    >>> payload_boolean()
    {'type': 'Property', 'value': True}
    """
    return {"type": "Property", "value": fake_boolean()}


def parse_schema_description(description) -> Tuple[Dict, str]:
    """
    Parses the schema description and extracts relevant information.

    Parameters:
    - description (str): The description string to be parsed.

    Returns:
    - tuple[dict, str]: A tuple contains a dictionary of NGSI type metadata and description.

    Example:
    >>> parse_schema_description("Property. This is a xxx. Model: 'TemperatureSensorModel'. Enum: 'High', 'Low'. Privacy: 'High'")
    [{"type": "Property", "model": "TemperatureSensorModel", "enum": ['High', 'Low'], "privacy": "High"}, "This is a xxx."]
    """
    ngsiOutput = {}

    # Process the description: remove the double-quotes, add spaces between sentences
    description = description.replace(chr(34), "")
    description = re.sub(r'\.([A-Z])', r'. \1', description)

    description = description.split(". ")
    copiedDescription = list.copy(description)

    for item in description:
        if item in propertyTypes:
            ngsiOutput["type"] = item
            copiedDescription.remove(item)
        elif item.find("Model:") > -1:
            copiedDescription.remove(item)
            ngsiOutput["model"] = (item.replace("'", ""))[len("Model:"):]
        elif item.find("Units:") > -1:
            copiedDescription.remove(item)
            ngsiOutput["units"] = (item.replace("'", ""))[len("Units:"):]
        elif item.find("Enum:") > -1:
            copiedDescription.remove(item)
            raw = (item.replace("'", ""))[len("Enum:"):]
            ngsiOutput["enum"] = raw.split(", ")
        elif item.find("Privacy:") > -1:
            copiedDescription.remove(item)
            ngsiOutput["privacy"] = (item.replace("'", ""))[len("Privacy:"):]

    description = ". ".join(copiedDescription)

    return ngsiOutput, description


def echo(concept: str, variable) -> None:
    """
    Print a formatted representation of a variable.

    Parameters:
    - concept (str): A string describing the concept of the variable.
    - variable: The variable to be printed.

    Example:
    >>> echo("Title", "Hello, World!")
    *** Title ***
    Hello, World!
    --- Title ---
    """
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def fake_array(type: str, numItems: int, options=None) -> list:
    """
    Generate an array of fake data based on the specified type and options.

    Parameters:
    - type (str): Type of elements in the array (e.g., "number", "boolean", "string", "date-time", "enum", "array", "object").
    - numItems (int): Number of items to generate in the array.
    - options (tuple, int, list, or dict): Options specific to the chosen type.

    Returns:
    - list: Array of fake data.

    Example:
    >>> fake_array("number", 3, (6, 0, 100))
    [45.2, 18.6, 97.0]

    TODO
    To be implemented based on the type and options of the items in the array
    To be implemented based on the structure of the object
    """
    if type == "number":
        return [fake_number(options) for _ in range(numItems)]
    elif type == "boolean":
        return [fake_boolean() for _ in range(numItems)]
    elif type == "string":
        return [fake_string(options) for _ in range(numItems)]
    elif type == "date-time":
        return [fake_datetime() for _ in range(numItems)]
    elif type == "enum":
        return [fake_enum(options) for _ in range(numItems)]
    elif type == "array":
        return []
    elif type == "object":
        return []

def payload_array(type: str, numItems: int, options) -> dict:
    """
    Generate a payload for an array property.

    Parameters:
    - type (str): Type of elements in the array ("number", "boolean", "string", "date-time", "enum", "array", "object").
    - numItems (int): Number of items to generate in the array.
    - options (tuple, int, list, or dict): Options specific to the chosen type.
        options for type number is a tuple with (length, minimum and maximum)
        options for type string is an integer with the length in paragraphs
        options for type enum is the list with the possible values
        options for array is a list with two values [type for the items, options for this type of item]
        options for object is the complete payload

    Returns:
    - dict: Property payload.

    Example:
    >>> payload_array("number", 3, (6, 0, 100))
    {'type': 'Property', 'value': [45.2, 18.6, 97.0]}
    """
    if type is not "array" and type is not "object":
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
        # [description, Property/Relationship/GeoProperty, Model, Units, Enum, Privacy]
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
    elif metadata[1] == "GeoProperty":
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

def parse_property2ngsild_example(fullPayload: dict, dataModel: str, level: int = 0) -> dict:
    """
    Recursively parse a JSON schema property and generate fake data in NGSI-LD format.

    Parameters:
    - fullPayload (dict): Full payload of the property.
    - dataModel (str): Name of the data model.
    - level (int): Level of recursion.

    Returns:
    - dict: Parsed property with generated fake data.

    Example:
    >>> parse_property2ngsild_example({"id": {"type": "string"}}, "ExampleDataModel", 0)
    {'id': {'type': 'Property', 'value': 'urn:ngsi-ld:ExampleDataModel:id:?????########'}}

    """
    prop = [p for p in fullPayload.keys()][0]
    payload = fullPayload[prop]

    # Get all the keys within this property
    keys = [k for k in payload]

    # Ignore `required` so far
    if "required" in keys:
        del fullPayload[prop]["required"]

    if "description" in keys:
        # parse description of the property
        # return a list, [description, Property/Relationship/GeoProperty, Model, Units, Enum, Privacy]
        ngsiOutput, description = parse_schema_description(payload["description"])
        metadata = [description, ngsiOutput["type"]]
    else:
        metadata = ["", "Property"]

    if prop == "id" and level == 0:
        # first level `id` is a system-defined property, displayed in key-value format by default
        return {"id": fake_uri("id", dataModel)}

    elif prop == "id" and level > 0:
        return payload_uri("id", dataModel)

    elif "patternProperties" in keys:
        # if `patternProperties` is defined, use the first pattern to generate
        keyPatterned = list(payload["patternProperties"].keys())[0]
        propertyName = rstr.xeger(keyPatterned)
        if "required" in fullPayload[prop]:
            del fullPayload[prop]["required"]
        return parse_property2ngsild_example({propertyName: fullPayload[prop]["patternProperties"][keyPatterned]},
                                             dataModel, level + 1)

    elif prop == "type" and level == 0:
        # first level `type` is a system-defined property, displayed in key-value format by default
        # `enum` is a key inside `type`, store the name of the data model
        # it is an error if `enum` is not found
        if "enum" in fullPayload[prop]:
            return fullPayload[prop]["enum"][0]
        else:
            return missingEntity

    elif prop == "location" or metadata[1] == "GeoProperty":
        # `location` or `GeoProperty`-like is displayed as `Point` by default
        return payload_geoproperty("Point")

    elif metadata[1] == "Relationship":
        # TODO only able to return Relationship in string, not in array or object
        return payload_relationship(prop, dataModel)

    elif prop in ["anyOf", "allOf", "oneOf"]:
        # take the first one in the structure to generate, consider as the same level
        return parse_property2ngsild_example({"item": fullPayload[prop][0]}, dataModel, level)

    elif "type" in keys:  # generate property according to its type

        if payload["type"] == "number":
            # treating number with/without maximum/minimum
            argsNumber = (4,)
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
            # treating integer with/without maximum/minimum
            argsNumber = ()
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
            # treat string with specific format defined
            if payload["format"] == "date-time":
                return payload_datetime()
            elif payload["format"] == "date":
                return payload_date()
            elif payload["format"] == "time":
                return payload_time()
            elif payload["format"] == "uri":
                return payload_uri(prop, dataModel)
            elif (payload["format"] == "idn-email") or (payload["format"] == "email"):
                return payload_email(dataModel)
            elif payload["format"] == "text":
                return payload_string(1)
            else:  # some format we couldn't generate for now
                return {"type": "Property", "value": "This is a certain format we couldn't generate for now."}

        elif payload["type"] == "string" and "enum" in keys:
            # treat string with enum defined, take only one
            return payload_enum(payload["enum"], 1)

        elif payload["type"] == "string":
            # treat normal string with minLength, maxLength, and pattern
            if "minLength" in payload:
                argsMin = int(payload["minLength"])
            else:
                argsMin = 0
            if "maxLength" in payload:
                argsMax = int(payload["maxLength"])
            else:
                argsMax = 200
            if "pattern" in payload:
                argsPattern = payload["pattern"]
            else:
                argsPattern = ""
            return payload_string(1, argsMin, argsMax, argsPattern)

        elif payload["type"] == "boolean":
            # treat boolean
            return payload_boolean()

        elif payload["type"] == "array":
            # treat array with minItems/maxItems/uniqueItems
            if "minItems" in payload:
                arrayItems = payload["minItems"]
            else:
                arrayItems = 2
            if "maxItems" in payload:
                arrayItems = int((arrayItems + int(payload["maxItems"])) / 2)
            else:
                arrayItems = arrayItems
            if "uniqueItems" in payload:
                uniqueItems = payload["uniqueItems"]
            else:
                uniqueItems = False  # False by default
            arrayPayload = payload["items"].copy()
            if "required" in arrayPayload:
                del arrayPayload["required"]

            valuesArray = []
            idx = 0
            while len(valuesArray) < arrayItems:
                # naive while-loop deals with uniqueItems if it is true
                tmp_value = parse_property2ngsild_example({"items": arrayPayload}, dataModel, level + 1)["value"]
                if uniqueItems and tmp_value in valuesArray:
                    continue
                else:
                    valuesArray.append(tmp_value)

                idx += 1
                if idx >= arrayItems * 5:  # max number of trying
                    # there may be the schema error
                    print("Scheme Error!")
                    break

            return {"type": "Property", "value": valuesArray}

        elif payload["type"] == "object":
            # treat object
            valuesObject = {}
            objectPayload = payload["properties"]
            if "required" in objectPayload:  # ignore required
                del objectPayload["required"]

            for p in objectPayload:  # generate properties for the object
                # only take the `value` to simplify the output, `object` if it's a Relationship
                objectOutput = parse_property2ngsild_example({p: objectPayload[p]}, dataModel, level + 1)
                if objectOutput["type"] == "Relationship":
                    valuesObject[p] = objectOutput["object"]
                else:
                    valuesObject[p] = objectOutput["value"]

            return {"type": "Property", "value": valuesObject}

    elif "oneOf" in keys:
        return parse_property2ngsild_example({prop: fullPayload[prop]["oneOf"][0]}, dataModel, level)

    elif "anyOf" in keys:
        return parse_property2ngsild_example({prop: fullPayload[prop]["anyOf"][0]}, dataModel, level)

    else:
        # other cases
        return {prop: pendingToImplement, "value": fake_uri(prop, dataModel)}

#########################################
#   Data model check related
#########################################

def merge_duplicate_attributes(dict_a: dict, dict_b: dict) -> dict:
    """
    Merge two dictionaries where the values are lists, combining duplicate keys.

    Parameters:
        dict_a (dict): The first dictionary to be merged.
        dict_b (dict): The second dictionary to be merged.

    Returns:
        dict: A new dictionary containing merged values for common keys.

    Example:
    >>> dict_a = {"1": [], "2": ["aa", "bb"]}
    >>> dict_b = {"1": [], "2": ["cc"], "3": ["dd"]}
    >>> merge_duplicate_attributes(dict_a, dict_b)
    {"1": [], "2": ["aa", "bb", "cc"], "3": ["dd"]}
    """
    for key, values in dict_b.items():
        # If the key exists in dict_a, extend its list with values from dict_b
        # If the key doesn't exist, create a new entry with values from dict_b
        dict_a[key] = dict_a.get(key, []) + values
    return dict_a

def parse_payload_v2(schemaPayload, level: int = 1) -> Tuple[Dict, Dict]:
    """
    Parse the given JSON schema payload recursively.

    Parameters:
        schemaPayload: The JSON schema payload to be parsed. could be dict or list
        level (int): The recursion level.

    Returns:
        tuple[dict, dict]: A tuple containing the parsed output and attributes.
    """
    output = {}
    attributes = {level: []}

    def process_allOf_oneOf_anyOf(ofSubSchema):
        nonlocal attributes, output
        for index in range(len(ofSubSchema)):
            partialOutput, partialAttr = parse_payload_v2(ofSubSchema[index], level + 1)
            output = dict(output,
                          **partialOutput["properties"] if "properties" in ofSubSchema[index] else partialOutput)
            attributes = merge_duplicate_attributes(attributes, partialAttr)

    if level == 1:  # first level starts always with "allOf", "properties", "anyOf", "oneOf"

        keys_to_check_level_one = ["allOf", "anyOf", "oneOf", "properties"]
        for key in keys_to_check_level_one:
            if key in schemaPayload:

                # if key is properties, then the value of the key is the sub-structure that needs to be extracted
                # same for "allOf", "anyOf", "oneOf", since their value type is always a list, so process the list first
                # Example
                # {"properties": {...}}
                # {"allOf": [{...}, {...}]}
                if key == "properties":
                    output, partialAttr = parse_payload_v2(schemaPayload[key], level + 1)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)
                else:
                    process_allOf_oneOf_anyOf(schemaPayload[key])

    elif level < 8:  # level from 2 to 8 will be processed as below, in case of the infinite loop or too massive schema

        # if schema is a list, then process the list first, take each element as a sub-schema
        # Example: [{...}, {...}, ...]
        if isinstance(schemaPayload, list):
            for index in range(len(schemaPayload)):
                partialOutput, partialAttr = parse_payload_v2(schemaPayload[index], level + 1)
                output = dict(output, **partialOutput)
                attributes = merge_duplicate_attributes(attributes, partialAttr)

        # if schema is a dictionary, then go inside directly
        # Example: {"allOf": [{...}, ...], "properties": {...}, "description": "xxxx", ...}
        if isinstance(schemaPayload, dict):

            for subschema in schemaPayload:  # run through each key

                if subschema in ["allOf", "anyOf", "oneOf"]:
                    output[subschema] = []
                    for index in range(len(schemaPayload[subschema])):
                        partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][index], level + 1)
                        output[subschema].append(
                            partialOutput["properties"] if "properties" in schemaPayload[subschema][
                                index] else partialOutput)
                        attributes = merge_duplicate_attributes(attributes, partialAttr)

                # Extract "prop1", "prop2" as the example given below
                # Example: {"properties": {"prop1": {...}, "prop2": {...}}}
                elif subschema == "properties":

                    output[subschema] = {}
                    for prop in schemaPayload["properties"]:

                        try:
                            output[subschema][prop]
                        except:
                            output[subschema][prop] = {}
                            attributes[level].append(prop)  # get the list of extracted properties per level

                        # process the specific sub-structure of a found property
                        for item in list(schemaPayload["properties"][prop]):

                            # get everything in allOf, anyOf, oneOf under a property
                            if item in ["allOf", "anyOf", "oneOf"]:
                                output[subschema][prop][item] = []
                                for index in range(len(schemaPayload[subschema][prop][item])):
                                    partialOutput, partialAttr = parse_payload_v2(
                                        schemaPayload[subschema][prop][item][index], level + 1)
                                    output[subschema][prop][item].append(partialOutput)
                                    attributes = merge_duplicate_attributes(attributes, partialAttr)

                            # parse the description, return a list [description, NGSI type, model name, unit name, enum, privacy]
                            elif item == "description":
                                x_ngsi, description = parse_schema_description(schemaPayload[subschema][prop][item])
                                output[subschema][prop][item] = description
                                if x_ngsi:
                                    output[subschema][prop]["x-ngsi"] = x_ngsi

                            # parse the sub-structure if equals to items or properties
                            elif item in ["items", "properties"]:
                                output[subschema][prop][item], partialAttr = parse_payload_v2(
                                    schemaPayload[subschema][prop][item], level + 1)
                                attributes = merge_duplicate_attributes(attributes, partialAttr)

                            # change the type integer to number
                            elif item == "type":
                                output[subschema][prop][item] = "number" if schemaPayload[subschema][prop][
                                                                                item] == "integer" else \
                                schemaPayload[subschema][prop][item]

                            # remain the rest part the same
                            else:
                                output[subschema][prop][item] = schemaPayload[subschema][prop][item]

                # if equals to description, parse it
                elif subschema == "description":
                    x_ngsi, description = parse_schema_description(schemaPayload[subschema])
                    output[subschema] = description
                    if x_ngsi:
                        output["x-ngsi"] = x_ngsi

                # for the subschema that is a dictionary, parse the inside
                elif isinstance(schemaPayload[subschema], dict):
                    attributes[level].append(subschema)
                    output[subschema], partialAttr = parse_payload_v2(schemaPayload[subschema], level + 1)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)

                # for the rest, remain the same
                else:
                    output[subschema] = schemaPayload[subschema]

    else:  # return None when parsing over 8 levels
        return None, None

    return output, attributes

def parse_yamlDict(yamlDict, datamodelRepoUrl: str, level: int = 1) -> dict:
    """
    Check the properties of descriptions, NGSI types, etc

    Parameters:
    - yamlDict (dict or list): The YAML dictionary to parse.
    - datamodelRepoUrl (str): The URL of the data model repository.
    - level (int, optional): The nesting level in the YAML structure. Defaults to 1.

    Returns:
    dict: A dictionary containing the extracted properties following the check results.

    Example:
        yamlDict = {"prop1": {"description": xxx, "type": "string", "x-ngsi": {"type": "Property"}, ...}, "prop2": ...}
        parse_yamlDict(yamlDict, datamodelRepoUrl)
    {
        "prop1": {
            "x-ngsi": true,
            "x-ngsi_text": "ok to Property",
            "documented": true,
            "text": "xxx"
        },
        "prop2": ...
    }
    """
    output = {}

    # if the yamlDict is a list, then parse it individually
    if isinstance(yamlDict, list):
        for item in yamlDict:
            partialoutput = parse_yamlDict(item, datamodelRepoUrl, level + 1)
            output = dict(output, **partialoutput)

    else:

        for prop in yamlDict:

            if prop == "id": continue

            # Example: [{...}, {...}, ...]
            if isinstance(yamlDict[prop], list) and len(yamlDict[prop]) > 1 and isinstance(yamlDict[prop][0], dict):
                for item in yamlDict[prop]:
                    partialoutput = parse_yamlDict(item, datamodelRepoUrl, level + 1)
                    output = dict(output, **partialoutput)

            # Example: {"description": xxx, "properties": xxx, "x-ngsi": xxx, ...}
            if isinstance(yamlDict[prop], dict):

                # if prop equals to any value of "properties", "allOf", "oneOf", "anyOf", "items"
                # means the value of prop has deeper structure, like dictionary or list
                # so need to parse it one level deeper
                if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                    partialoutput = parse_yamlDict(yamlDict[prop], datamodelRepoUrl, level + 1)
                    output = dict(output, **partialoutput)
                    continue

                # Process the substructures
                # Get the keys inside
                # Examples: {"description": xxx, "properties": xxx, "x-ngsi": xxx, ...}
                # --> ["description", "properties", "x-ngsi", ...]
                for propKey in yamlDict[prop].keys():
                    if propKey in ["properties", "anyOf", "allOf", "oneOf", "items"]:
                        partialoutput = parse_yamlDict(yamlDict[prop][propKey], datamodelRepoUrl, level + 1)
                        output = dict(output, **partialoutput)

                # prop is a real property except it equals to `x-ngsi` and inside of exceptions, exceptions = ["coordinates", "bbox", "type"]
                # "x-ngsi": {"type": "Property",  "model": xxx}
                # exceptions: no descriptions and no NGSI type claimed
                if prop != "x-ngsi" and not prop in exceptions:

                    try:
                        # Process the NGSI type, have to be one of the three ["Property", "Relationship", "GeoProperty"]
                        propertyType = yamlDict[prop]["x-ngsi"]["type"]

                        if propertyType in propertyTypes:
                            output[prop] = {}
                            output[prop]["x-ngsi"] = True
                            output[prop]["x-ngsi_text"] = "ok to " + str(propertyType)
                        else:
                            output[prop]["x-ngsi"] = False
                            output[prop][
                                "x-ngsi_text"] = "Wrong NGSI type of " + propertyType + " in the description of the property on level " + str(
                                level)

                    except:
                        output[prop] = {}
                        output[prop]["x-ngsi"] = False
                        output[prop]["x-ngsi_text"] = "Missing NGSI type of " + str(
                            propertyTypes) + " in the description of the property on level " + str(level)

                    try:
                        # checking the pure description whether is well-documented
                        description = yamlDict[prop]["description"]

                        if len(description) > 15:  # if the description is longer than 15 char then it is well-documented
                            output[prop]["documented"] = True
                            output[prop]["text"] = description
                        else:
                            output[prop]["documented"] = False
                            output[prop]["text"] = incompleteDescription

                    except:
                        output[prop]["documented"] = False
                        output[prop]["text"] = withoutDescription

                    if prop == "type" and level == 1:

                        try:
                            # Type property matches data model name
                            propertyType = yamlDict[prop]["enum"]

                            if propertyType[0] == extract_datamodel_from_raw_url(datamodelRepoUrl):
                                output[prop]["type_specific"] = True
                                output[prop][
                                    "type_specific_text"] = "Type property matches to data model name on level " + str(
                                    level)
                            else:
                                output[prop]["type_specific"] = False
                                output[prop][
                                    "type_specific_text"] = "Type property doesn't match to data model name on level " + str(
                                    level)

                        except:
                            output[prop]["type_specific"] = False
                            output[prop]["type_specific_text"] = "Missing Type property"

    return output

def is_metadata_properly_reported(output: dict, schemaDict: dict) -> dict:
    """
    Check if metadata (derivedFrom and license) is properly reported in the output based on the given JSON schema.

    Parameters:
    - output (dict): The output dictionary to report metadata warnings.
    - schemaDict (dict): The schema dictionary containing information about the schema.

    Returns:
    - dict: The updated output dictionary with metadata warnings.

    Example:
    >>> schema = {"derivedFrom": "https://example.com/base_schema", "license": "https://example.com/license"}
    >>> is_metadata_properly_reported({}, schema)
    {'metadata': {'derivedFrom': {'warning': 'derivedFrom is not a valid url'},
                  'license': {'warning': 'License is not a valid url. It should be a link to the license document'}}}

    """
    if "metadata" not in output:
        output["metadata"] = {}

    metadata_fields = ["derivedFrom", "license"]

    for field in metadata_fields:
        try:
            # if field not in output["metadata"]:
            #     output["metadata"][field] = {}

            if field in schemaDict:
                value = schemaDict[field]

                if value:
                    if not checkers.is_url(value):
                        # check url format
                        output["metadata"][field] = {"warning": f"{field} is not a valid URL"}
                    elif not is_url_existed(value)[0]:
                        # check the url reachability
                        output["metadata"][field] = {"warning": f"{field} URL is not reachable"}
                else:
                    output["metadata"][field] = {"warning": f"{field} is empty"}
            else:
                output["metadata"][field] = {"warning": f"Missing {field} clause, include {field} = '' in the header"}
        except Exception as e:
            output["metadata"][field] = {"warning": f"not possible to check {field} clause, {str(e)}"}

    return output

def is_metadata_existed(output: dict, jsonDict: dict, schemaUrl: str, message: str = "", checkall: bool = True,
                        checklist: list = None) -> dict:
    """
    Check if metadata (e.g., $schema, $id, title, description, modelTags, schemaVersion, required) is properly reported
    in the output based on the given schema dictionary.

    Parameters:
    - output (dict): The output dictionary to report metadata warnings.
    - jsonDict (dict): The schema dictionary containing information about the schema.
    - schemaUrl (str): The URL of the schema.
    TODO: extend function with three parameters below
    - message (str): Custom message.
    - checkall (bool): If True, check all metadata; if False, use the checklist.
    - checklist (list): List of metadata items to check.

    Returns:
    - dict: The updated output dictionary with metadata warnings.

    Example:
    >>> schema = {"$schema": "http://json-schema.org/schema#", "$id": "https://example.com/schema", "title": "Example Schema"}
    >>> is_metadata_existed({}, schema, "https://example.com/schema")
    {'metadata': {'$schema': {'warning': '$schema should be "http://json-schema.org/schema#" by default'},
                  '$id': {'warning': '$id doesn't match, please check it again'},
                  'title': {'warning': 'Title too short'},
                  'description': {'warning': 'Description is empty'},
                  'modelTags': {'warning': 'Missing modelTags clause, include modelTags = \'\' in the header'},
                  'schemaVersion': {'warning': 'Schema version format wrong. Right is x.x.x'},
                  'required': {'warning': 'Too many required attributes, consider its reduction to less than 5 preferably just id and type'}}}

    """
    if "metadata" not in output:
        output["metadata"] = {}

    metadata_fields = {
        "$schema": {"type": "string", "value": "http://json-schema.org/schema#"},
        "$id": {"type": "string", "value": schemaUrl},
        "title": {"type": "string", "min_length": 15},
        "description": {"type": "string", "min_length": 34},
        "modelTags": {"type": "string"},
        "$schemaVersion": {"type": "string", "pattern": "^\d{1,3}.\d{1,3}.\d{1,3}$"},
        "required": {"type": "list", "default": ["id", "type"], "max_length": 4, "mandatory_fields": ["id", "type"]}
    }

    for field, constraints in metadata_fields.items():
        try:
            # if field not in output["metadata"]:
            #     output["metadata"][field] = {}

            if field in jsonDict:
                value = jsonDict[field]

                # match with the type
                if constraints["type"] == "string":
                    if not isinstance(value, str):
                        output["metadata"][field] = {"warning": f"{field} is not a string"}
                elif constraints["type"] == "list":
                    if not isinstance(value, list):
                        output["metadata"][field] = {"warning": f"{field} is not a list"}

                # match with the value
                if "value" in constraints:
                    if value != constraints:
                        if field == "$schema":
                            output["metadata"][field] = {"warning": f"{field} should be {constraints} by default"}
                        elif field == "$id" and (KEYWORDS_FOR_CERTAIN_CHECK in constraints):
                            output["metadata"][field] = {
                                "warning": f"{field} doesn't match, please check it again or ignore this message if it's an unpublished datamodel"}

                # min_length
                if "min_length" in constraints and len(value) < constraints["min_length"]:
                    output["metadata"][field] = {"warning": f"{field} is too short"}

                # max_length
                if "max_length" in constraints and len(value) > constraints["max_length"]:
                    output["metadata"][field] = {"warning": f"{field} is too long"}

                # pattern
                if "pattern" in constraints and re.search(constraints["pattern"], value) is None:
                    output["metadata"][field] = {"warning": f"{field} format wrong. Right is x.x.x. Default = 0.0.1"}

                # mandatory_field
                if "mandatory_fields" in constraints:
                    for mf in constraints["mandatory_fields"]:
                        if mf not in value:
                            output["metadata"][field] = {
                                "warning": f"{field} should include {', '.join(constraints['mandatory_fields'])}"}
            else:
                output["metadata"][field] = {"warning": f"Missing {field} clause, include {field} = '' in the header"}
        except Exception as e:
            output["metadata"][field] = {"warning": f"not possible to check {field} clause, {str(e)}"}

    return output

def schema_output_sum(output: dict) -> dict:
    """
    Summarize the output of a schema validation process, categorizing properties and metadata, especially for the failed cases.

    Parameters:
    - output (dict): The output dictionary from a schema validation process.

    Returns:
    - dict: A summary dictionary categorizing properties and metadata.

    Example:
        validation_output = {...}  # An example output from a schema validation process
        schema_output_summary(validation_output)
    {
        'well documented': [...],
        'already used': [...],
        'newly available': [...],
        'Metadata': [...],
        'Failed': {
            'Failed reason 1': [...],
            'Failed reason 2': [...],
            ...
        },
        ...
    }
    """
    documentationStatusOfProperties = output['documentationStatusOfProperties']
    alreadyUsedProperties = output['alreadyUsedProperties']
    availableProperties = output['availableProperties']
    metadata = output['metadata']

    results = {}
    results = {key: [] for key in CHECKED_PROPERTY_CASES}
    results['Failed'] = {}

    for prop, value in documentationStatusOfProperties.items():

        if value['documented'] & value['x-ngsi']:
            # Only if the `documented` and NGSI type are True
            results['well documented'].append(prop)

        else:
            if value['x-ngsi'] is False:
                # If NGSI type is False
                if value['x-ngsi_text'] not in results['Failed'].keys():
                    results['Failed'][value['x-ngsi_text']] = []
                results['Failed'][value['x-ngsi_text']].append(prop)

            if value['documented'] is False:
                # If documented is False
                if value['text'] not in results['Failed'].keys():
                    results['Failed'][value['text']] = []
                results['Failed'][value['text']].append(prop)

        if (prop == "type") and (value["type_specific"] is False):
            # If the property is `type`, then it has to be in the same as datamodel
            # If it is different, then `type_specific` is False
            results['Failed'][value["type_specific_text"]] = []
            results['Failed'][value["type_specific_text"]].append(prop)

        if 'duplicated_prop' in value:
            # Collect duplicated properties
            try:
                results['Failed'][value['duplicated_prop_text']].append(prop)
            except:
                results['Failed'][value['duplicated_prop_text']] = []
                results['Failed'][value['duplicated_prop_text']].append(prop)

    for prop in alreadyUsedProperties:
        results['already used'].append(list(prop.keys())[0])

    for prop in availableProperties:
        results['newly available'].append(list(prop.keys())[0])

    for prop, value in metadata.items():
        results['Metadata'].append(value['warning'])

    return results

def message_after_check_schema(results: dict) -> str:
    """
    Generate a summary message based on the results of a schema validation check.

    Parameters:
    - results (dict): The summarized results from schema validation.

    Returns:
    - str: A message providing information about different property categories and metadata warnings.

    Example:
    >>> validation_results = {...}  # An example of summarized validation results
    >>> message_after_check_schema(validation_results)
    '
    These properties are well documented properties:

        dateCreated, dateModified, source, name, ...

    These properties are already used properties:

        openingHoursSpecification, startDate, ...

    No big issue with the named properties in general.

    Some warnings related to metadata:

    ...
    '
    """
    message = ""

    for key in CHECKED_PROPERTY_CASES[:-2]:
        if results[key]:
            message += f"\nThese properties are {key} properties:\n    {newline.join(results[key])}"

    # Include messages for properties with failures
    if results[CHECKED_PROPERTY_CASES[-1]]:
        message += f"""
However, We highly suggest you fix these properties:
    {newline.join([" - " + text + newline + f"{', '.join(pps)}" for text, pps in results['Failed'].items()])}
        """
    else:
        message += "\nNo major issues with the named properties in general."

    # Include messages for metadata warnings
    if results[CHECKED_PROPERTY_CASES[-2]]:
        message += f"\nSome warnings related to metadata:\n    {newline.join([' - ' + text for text in results['Metadata']])}"
    else:
        message += "\nNo warnings with metadata."

    return message

def convert_to_raw_github_url(input_url):
    match = re.match(github_url_pattern, input_url)
    
    if match:
        owner = match.group(1)
        repository = match.group(2)
        branch = match.group(3)
        file_path = match.group(4)
        raw_github_url = f"https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{file_path}"
        return raw_github_url
    else:
        print("Invalid GitHub URL format")