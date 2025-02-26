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

def resolve_ref(repo_path, ref, base_uri=""):
    """
    Resolve a $ref reference in the schema, handling both local and external references.

    Parameters:
        repo_path (str): The path to the schema.json file.
        ref (str): The reference to resolve (e.g., "#/definitions/SomeDefinition" or "common-schema.json#/definitions/SomeDefinition").
        base_uri (str): The base URI for resolving relative references.

    Returns:
        dict: The resolved schema fragment.
    """
    try:
        if "#" in ref:
            url_part, pointer_part = ref.split("#", 1)
        else:
            url_part, pointer_part = ref, ""

        if url_part.startswith("http"):
            # External reference (absolute URL)
            resolved_url = url_part
        elif url_part:
            # External reference (relative URL)
            resolved_url = urljoin(base_uri, url_part)
        else:
            # Local reference within the same file
            # Use the base URI to determine the file name
            if base_uri:
                resolved_url = base_uri
            else:
                # Fallback to the primary schema file in the repo path
                resolved_url = os.path.join(repo_path, "schema.json")

        # Fetch the schema
        if resolved_url.startswith("http"):
            response = requests.get(resolved_url)
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch external schema from {resolved_url}")
            schema = response.json()
        else:
            with open(resolved_url, 'r') as file:
                schema = json.load(file)

        # Resolve the JSON Pointer if it exists
        if pointer_part:
            try:
                schema = resolve_pointer(schema, pointer_part)
            except Exception as e:
                raise ValueError(f"Failed to resolve JSON Pointer '{pointer_part}' in schema: {e}")

        # Recursively resolve any nested $refs in the resolved schema
        # Use the resolved URL as the base URI for nested $refs
        schema = resolve_nested_refs(schema, resolved_url if url_part else base_uri)

        return schema
    except Exception as e:
        raise ValueError(f"Error resolving reference {ref}: {e}")

def resolve_nested_refs(schema, base_uri):
    """
    Recursively resolve any nested $refs in the schema.
    """
    if isinstance(schema, dict):
        if "$ref" in schema:
            return resolve_ref("", schema["$ref"], base_uri)
        else:
            for key, value in schema.items():
                schema[key] = resolve_nested_refs(value, base_uri)
    elif isinstance(schema, list):
        for i, item in enumerate(schema):
            schema[i] = resolve_nested_refs(item, base_uri)

    return schema

def validate_properties(repo_path, properties, base_uri, path="", success=True, output=[]):
    """
    Recursively validate properties in the schema, ensuring that arrays have 'items' and objects have 'properties'.

    Parameters:
        repo_path (str): The path to the schema.json file.
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
                    resolved = resolve_ref(repo_path, value["$ref"], base_uri)
                    success, output = validate_properties(repo_path, resolved, base_uri, current_path, success, output)
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
                success, output = validate_properties(repo_path, value["properties"], base_uri, current_path + ".", success, output)
            if "items" in value and isinstance(value["items"], dict):
                success, output = validate_properties(repo_path, value["items"], base_uri, current_path + ".", success, output)

    return success, output

def test_array_object_structure(repo_path, options):
    """
    Validate that attributes with type 'array' have an 'items' clause and
    attributes with type 'object' have a 'properties' clause, handling allOf and $ref.

    Parameters:
        repo_path (str): The path to the schema.json file.
        options (dict): Additional options for the test (unused in this test).

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking array and object attributes structure"
    success = True
    output = []

    try:
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        base_uri = schema.get("$id", "")  # Use $id as the base URI for resolving relative $refs

        # Handle allOf clause
        if "allOf" in schema and isinstance(schema["allOf"], list):
            for item in schema["allOf"]:
                if isinstance(item, dict) and "properties" in item:
                    success, output = validate_properties(repo_path, item["properties"], base_uri, "", success, output)
        elif "properties" in schema and isinstance(schema["properties"], dict):
            success, output = validate_properties(repo_path, schema["properties"], base_uri, "", success, output)

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output