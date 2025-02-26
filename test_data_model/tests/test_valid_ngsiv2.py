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
#  Author: Alberto Abella                                                       #
#################################################################################
# version 26/02/25 - 1

import json

def validate_entity(entity):
    """
    Validate that the 'id' is a URI and 'type' is a string.

    Parameters:
        entity (dict): The JSON object to validate.

    Returns:
        tuple: (success: bool, message: list)
    """
    success = True
    messages = []

    # Validate 'id' as a URI
    if "id" in entity:
        if not isinstance(entity["id"], str):
            success = False
            messages.append(f"*** 'id' value '{entity['id']}' is NOT a valid URI")
    else:
        success = False
        messages.append("*** Missing 'id' key")

    # Validate 'type' as a string
    if "type" in entity:
        if not isinstance(entity["type"], str):
            success = False
            messages.append(f"*** 'type' value '{entity['type']}' is NOT a string")
    else:
        success = False
        messages.append("*** Missing 'type' key")

    return success, messages


def test_valid_ngsiv2(repo_path, options):
    """
    Validate if the example-normalized.json file is a valid NGSI v2 file in normalized format.

    Parameters:
        repo_path (str): The path to the directory where the files are located.

    Returns:
        tuple: (test_name: str, success: bool, message: str)
    """
    test_name = "Validating example-normalized.json as NGSI v2 normalized format"
    success = True
    output = []


#    Example usage of the options parameter (optional, for future flexibility)
#    if options.get("published", False):
#        unpublished = True
#    if options.get("private", False):
#        output.append("This is a private model.")


    try:
        # Load the example-normalized.json file
        with open(f"{repo_path}/examples/example-normalized.json", 'r') as file:
            data = json.load(file)

        success, output = validate_entity(data)

        # Validate the structure of the NGSI v2 normalized format
        required_fields = ["id", "type"]
        for entity in data:
            if entity in required_fields:
                continue
            # Check for required fields in each entity
            if not isinstance(data[entity], dict):
                success = False
                output.append(f"*** {entity} have incomplete structure")
            else:
                if "type" not in data [entity]:
                    success = False
                    output.append(f"*** {entity} has not type")
                if "value" not in data [entity]:
                    success = False
                    output.append(f"*** {entity} has not value")
    except json.JSONDecodeError:
        success = False
        output.append("*** example-normalized.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** example-normalized.json file not found")

    return test_name, success, output