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
import os
import requests
from urllib.parse import urljoin
from jsonpointer import resolve_pointer
from .utils import resolve_ref

def validate_properties(repo_files, properties, base_uri, path="", success=True, output=[]):
    """
    Recursively validate properties in the schema, ensuring that arrays have 'items' and objects have 'properties'.

    Parameters:
        repo_files (dict): Dictionary containing loaded files.
        properties (dict): The properties to validate.
        base_uri (str): The base URI for resolving relative references.
        path (str): The current path in the schema (for error messages).
        success (bool): The current success status.
        output (list): The list of error messages.

    Returns:
        tuple: (success: bool, output: list)
    """
    for key, value in properties.items():
        current_path = f"{path}.{key}" if path else key

        if isinstance(value, dict):
            # Handle $ref references
            if "$ref" in value:
                try:
                    resolved = resolve_ref(repo_files, value["$ref"], base_uri)
                    success, output = validate_properties(repo_files, resolved, base_uri, current_path, success, output)
                except ValueError as e:
                    success = False
                    output.append(f"*** Error: Failed to resolve $ref in attribute '{current_path}': {e}")
                continue

            # Check type-specific clauses
            type_value = value.get("type", "")
            if type_value == "array" and "items" not in value:
                success = False
                output.append(f"*** Error: Attribute '{current_path}' is of type 'array' but is missing the 'items' clause.")
            elif type_value == "object" and "properties" not in value:
                success = False
                output.append(f"*** Error: Attribute '{current_path}' is of type 'object' but is missing the 'properties' clause.")

            # Recursively check nested properties
            if "properties" in value and isinstance(value["properties"], dict):
                success, output = validate_properties(repo_files, value["properties"], base_uri, current_path + ".", success, output)
            if "items" in value and isinstance(value["items"], dict):
                success, output = validate_properties(repo_files, value["items"], base_uri, current_path + ".", success, output)

    return success, output

def test_array_object_structure(repo_files, options):
    """
    Validate that attributes with type 'array' have an 'items' clause and
    attributes with type 'object' have a 'properties' clause, handling allOf and $ref.

    Parameters:
        repo_files (dict): Dictionary containing loaded files.
        options (dict): Additional options for the test (unused in this test).

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking array and object attributes structure"
    success = True
    output = []

    file_name = "schema.json"
    if file_name not in repo_files or repo_files[file_name] is None:
        success = False
        output.append("*** schema.json file not found")
        return test_name, success, output

    file_data = repo_files[file_name]
    if "json" not in file_data:
        success = False
        output.append("*** schema.json is not a valid JSON file")
        return test_name, success, output
    
    schema = file_data["json"]

    base_uri = schema.get("$id", "")  # Use $id as the base URI for resolving relative $refs

    # Handle allOf clause
    if "allOf" in schema and isinstance(schema["allOf"], list):
        for item in schema["allOf"]:
            if isinstance(item, dict) and "properties" in item:
                success, output = validate_properties(repo_files, item["properties"], base_uri, "", success, output)
    elif "properties" in schema and isinstance(schema["properties"], dict):
        success, output = validate_properties(repo_files, schema["properties"], base_uri, "", success, output)

    return test_name, success, output
