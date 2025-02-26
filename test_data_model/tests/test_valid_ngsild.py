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
import requests


def check_context_url(context):
    """
    Check if the @context URL(s) are valid by making an HTTP request.
    If @context is an array, check each URL individually.

    Parameters:
        context (str or list): The URL or list of URLs to check.

    Returns:
        tuple: (success, message)
            success (bool): True if all URLs are valid, False otherwise.
            message (str): A message describing the result of the check.
    """
    if isinstance(context, str):
        # Single URL case
        try:
            response = requests.get(context)
            if response.status_code == 200:
                return True, f"The @context URL '{context}' is valid."
            else:
                return False, f"*** The @context URL '{context}' does not return a valid response (HTTP {response.status_code})."
        except Exception as e:
            return False, f"*** The @context URL '{context}' is not reachable: {e}"
    elif isinstance(context, list):
        # Array of URLs case
        warnings = []
        for url in context:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    warnings.append(
                        f"*** The @context URL '{url}' does not return a valid response (HTTP {response.status_code}).")
            except Exception as e:
                warnings.append(f"*** The @context URL '{url}' is not reachable: {e}")

        if warnings:
            return False, "WARNING: " + " ".join(warnings) + " Ignore this if it is an unpublished data model."
        else:
            return True, "All @context URLs are valid."
    else:
        return False, "*** Invalid @context format. Expected a URL or an array of URLs."

def test_valid_ngsild(repo_path, options):
    """
    Validate if the example-normalized.jsonld file is a valid NGSI-LD file.

    Parameters:
        repo_path (str): The path to the directory where the files are located.

    Returns:
        tuple: (test_name: str, success: bool, message: str)
    """

    test_name = "Validating example-normalized.jsonld as NGSI-LD format"
    success = True
    output = []

    # List of valid attribute types
    valid_attribute_types = ["Property", "GeoProperty", "Relationship", "LanguageProperty", "ListProperty"]

    try:
        # Load the example-normalized.jsonld file
        with open(f"{repo_path}/examples/example-normalized.jsonld", 'r') as file:
            entity = json.load(file)

        # Validate that the root element is a single entity (a dictionary)
        if not isinstance(entity, dict):
            success = False
            output.append("*** The root element must be a single entity (a dictionary)")
        else:
            # Check for required fields in the entity
            required_fields = ["id", "type", "@context"]
            for field in required_fields:
                if field not in entity:
                    success = False
                    output.append(f"*** Entity is missing required field: {field}")


            # Check for the '@context' field
            if "@context" not in entity:
                success = False
                output.append("*** Entity is missing the '@context' field")
            else:
                success_context, context_message = check_context_url(entity["@context"])
                success = success_context and success
                output.append(context_message)

            # Check properties and relationships
            for key, value in entity.items():
                if key not in ["id", "type", "@context"]:
                    if not isinstance(value, dict):
                        success = False
                        output.append(f"*** Property/Relationship '{key}' must be a dictionary")


                    # Check for the 'type' field in the attribute
                    if "type" not in value:
                        success = False
                        output.append(f"*** Property/Relationship '{key}' is missing the 'type' field")


                    # Validate the attribute type
                    attribute_type = value.get("type")
                    if attribute_type not in valid_attribute_types:
                        success = False
                        output.append(f"*** Invalid attribute type '{attribute_type}' for '{key}'. Allowed types: {valid_attribute_types}")


                    # Handle LanguageProperty type
                    if attribute_type == "LanguageProperty":
                        if "languageMap" not in value:
                            success = False
                            output.append(f"*** LanguageProperty '{key}' is missing the 'languageMap' field")

                        # Check if 'value' or 'object' are present (they should not be)
                        if "value" in value or "object" in value:
                            success = False
                            output.append(f"*** LanguageProperty '{key}' should not contain 'value' or 'object' fields")

                    else:
                        # Handle other attribute types
                        if attribute_type == "Relationship":
                            if "object" not in value:
                                success = False
                                output.append(f"*** Relationship '{key}' is missing the 'object' field")

                        else:
                            if "value" not in value:
                                success = False
                                output.append(f"*** Property '{key}' is missing the 'value' field")


    except json.JSONDecodeError:
        success = False
        output.append("*** example-normalized.jsonld is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** example-normalized.jsonld file not found")

    return test_name, success, output