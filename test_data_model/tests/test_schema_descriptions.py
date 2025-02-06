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

import json
import os
import requests
from urllib.parse import urljoin

def validate_description(description):
    """
    Validate that the description follows the required format.
    - The description must include a mandatory NGSI type (Property, GeoProperty, or Relationship).
    - The NGSI type must not contain extra spaces.
    - Optional elements (Model, Units, Enum, Privacy, Multilingual) must follow the format Key:'value'.
    - The description must be at least 15 characters long.
    """
    # Check if the description is at least 15 characters long
    if len(description) < 15:
        return False, "*** Description must be at least 15 characters long."

    # Split the description into parts using '. ' as the separator
    parts = [part for part in description.split(". ")]
    # print(parts)

    # Check for the mandatory NGSI type in any part
    valid_ngsi_types = ["Property", "GeoProperty", "Relationship", "LanguageProperty", "ListProperty"]
    ngsi_type_found = None
    for part in parts:
        if part in valid_ngsi_types:
            ngsi_type_found = part
            break
     # If no exact NGSI type is found, check for a part with extra characters
    if not ngsi_type_found:
        for part in parts:
            for ngsi_type in valid_ngsi_types:
                # Check if the part contains the NGSI type with extra characters
                if ngsi_type in part and part != ngsi_type:
                    return False, f"NGSI type '{part}' contains extra characters."

        # If no NGSI type (exact or with extra characters) is found, return an error
        return False, "*** NGSI type is not described. Must be one of: Property, GeoProperty, Relationship, LanguageProperty, ListProperty"


    # If no NGSI type is found, return an error
    if not ngsi_type_found:
        return False, "*** NGSI type is not described. Must be one of: Property, GeoProperty, Relationship."

    # Check if the NGSI type contains extra spaces
  # Check if the NGSI type contains extra spaces
    if ngsi_type_found.strip() != ngsi_type_found:
        return False, f"*** NGSI type '{ngsi_type_found}' contains extra spaces."

    # Check optional elements (Model, Units, Enum, Privacy, Multilingual)
    optional_keys = ["Model:", "Units:", "Enum:", "Privacy:", "Multilingual"]
    for part in parts:
        for key in optional_keys:
            if part.startswith(key):
                # Check if the value is enclosed in single quotes immediately after the colon
                if not part[len(key):].startswith("'"):
                    return False, f"*** Invalid format for '{key}'. Expected format: {key}'value'."
                if not part.endswith("'"):
                    return False, f"*** Invalid format for '{key}'. Expected format: {key}'value'."

    # If all checks pass, the description is valid
    return True, "Description is valid."


def resolve_ref(ref, base_uri):
    """
    Resolve a $ref to its external schema and return the referenced schema.
    """
    if ref.startswith("http"):
        # Absolute URL
        response = requests.get(ref)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"*** Failed to fetch external schema from {ref}")
    else:
        # Relative URL
        resolved_url = urljoin(base_uri, ref)
        response = requests.get(resolved_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"*** Failed to fetch external schema from {resolved_url}")

def check_property_descriptions(properties, base_uri, output, path=""):
    """
    Recursively check descriptions for all properties, including nested ones and arrays.
    """
    for prop_name, prop_details in properties.items():
        current_path = f"{path}.{prop_name}" if path else prop_name

        if "$ref" in prop_details:
            # Resolve the $ref and check the referenced schema
            try:
                ref_schema = resolve_ref(prop_details["$ref"], base_uri)
                check_property_descriptions(ref_schema.get("properties", {}), base_uri, output, current_path)
            except ValueError as e:
                output.append(f"*** Error resolving $ref for property '{current_path}': {e}")
        elif "properties" in prop_details:
            # Recursively check nested properties
            check_property_descriptions(prop_details["properties"], base_uri, output, current_path)
        elif "items" in prop_details:
            # Handle arrays
            items = prop_details["items"]
            if "properties" in items:
                # Recursively check properties of array items (if items are objects)
                check_property_descriptions(items["properties"], base_uri, output, f"{current_path}.items")
            elif "items" in items:
                # Recursively check nested arrays
                check_property_descriptions({"items": items["items"]}, base_uri, output, current_path)
            else:
                # Check for a description in the items clause (for primitive types)
                if "description" not in items:
                    output.append(f"*** The attribute '{current_path}.items' is missing a description.")
                else:
                    # Validate the description
                    description = items["description"]
                    is_valid, message = validate_description(description)
                    if not is_valid:
                        output.append(f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                    else:
                        output.append(f"*** The attribute '{current_path}.items' is properly documented.")
        elif "description" not in prop_details:
            output.append(f"*** The attribute '{current_path}' is missing a description.")
        else:
            # Validate the description
            description = prop_details["description"]
            is_valid, message = validate_description(description)
            if not is_valid:
                output.append(f"*** The attribute '{current_path}' has an invalid description: {message}")
            else:
                output.append(f"The attribute '{current_path}' is properly documented.")

def test_schema_descriptions(repo_to_test):
    """
    Test that all elements in the schema.json file include a description and that the description is valid.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if all descriptions are valid, False otherwise.
        output (list): List of messages describing the results of the test.
    """
    schema_file = os.path.join(repo_to_test, "schema.json")
    if not os.path.exists(schema_file):
        return "Checking that the schema is properly described in all its attributes", False, ["Schema file not found."]

    with open(schema_file, 'r') as f:
        schema = json.load(f)

    output = []
    base_uri = schema.get("$id", "")  # Use $id as the base URI for resolving relative $refs

    # Check properties in the schema
    if "properties" in schema:
        check_property_descriptions(schema["properties"], base_uri, output)

    # Check properties in allOf, if present
    if "allOf" in schema:
        for item in schema["allOf"]:
            if "properties" in item:
                check_property_descriptions(item["properties"], base_uri, output)

    # Determine if the test was successful
    success = not any("invalid" in message or "missing" in message for message in output)

    test_name = "Checking that the schema is properly described in all its attributes"
    return test_name, success, output

# Example usage (for standalone testing)
#if __name__ == "__main__":
#    repo_to_test = "path/to/repo"  # Replace with the actual path to the repository
#    test_name, success, output = test_schema_descriptions(repo_to_test)
#    print(f"Test Name: {test_name}")
#    print(f"Success: {success}")
#    print("Output:")
#    for message in output:
#        print(message)

