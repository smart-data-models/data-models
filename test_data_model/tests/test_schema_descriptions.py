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
from json import load
from os.path import join, exists
from requests import get
from urllib.parse import urljoin
from jsonpointer import resolve_pointer
from itertools import product

def validate_description(description):
    """
    Validate that the description follows the required format.
    - The description must include a mandatory NGSI type (Property, GeoProperty, or Relationship).
    - The NGSI type must not contain extra spaces.
    - Optional elements (Model, Units, Enum, Privacy, Multilingual) must follow the format Key:'value'.
    - The description must be at least 15 characters long.
    """
    if len(description) < 15:
        return False, "*** Description must be at least 15 characters long."

    parts = list(description.split(". "))

    valid_ngsi_types = ["Property", "GeoProperty", "Relationship", "LanguageProperty", "ListProperty"]
    ngsi_type_found = None
    for part in parts:
        if part in valid_ngsi_types:
            ngsi_type_found = part
            break

    if not ngsi_type_found:
        return next(
            (
                (False, f"NGSI type '{part}' contains extra characters.")
                for part, ngsi_type in product(parts, valid_ngsi_types)
                if ngsi_type in part and part != ngsi_type
            ),
            (
                False,
                "*** NGSI type is not described. Must be one of: Property, GeoProperty, Relationship, LanguageProperty, ListProperty",
            ),
        )
    
    if ngsi_type_found.strip() != ngsi_type_found:
        return False, f"*** NGSI type '{ngsi_type_found}' contains extra spaces."

    optional_keys = ["Model:", "Units:", "Enum:", "Privacy:", "Multilingual"]
    for part, key in product(parts, optional_keys):
        if part.startswith(key):
            if not part[len(key):].startswith("'"):
                return False, f"*** Invalid format for '{key}'. Expected format: {key}'value'."
            if not part.endswith("'"):
                return False, f"*** Invalid format for '{key}'. Expected format: {key}'value'."

    return True, "Description is valid."

def resolve_ref(ref, base_uri):
    """
    Resolve a $ref to its external schema and return the referenced schema.
    Handles both remote URLs and JSON Pointers, and recursively resolves nested $refs.
    JSON Pointers (starting with #) are resolved relative to the schema being referenced.
    """
    url_part, pointer_part = ref.split("#", 1) if "#" in ref else (ref, "")
    if url_part.startswith("http"):
        resolved_url = url_part
    else:
        resolved_url = urljoin(base_uri, url_part)

    response = get(resolved_url)
    if response.status_code != 200:
        raise ValueError(f"*** Failed to fetch external schema from {resolved_url}")

    schema = response.json()

    if pointer_part:
        try:
            # Resolve the JSON Pointer relative to the fetched schema
            schema = resolve_pointer(schema, pointer_part)
        except Exception as e:
            raise ValueError(
                f"*** Failed to resolve JSON Pointer '{pointer_part}' in schema: {e}"
            ) from e

    # Recursively resolve any nested $refs in the resolved schema
    schema = resolve_nested_refs(schema, resolved_url if url_part else base_uri)

    return schema

def resolve_nested_refs(schema, base_uri):
    """
    Recursively resolve any nested $refs in the schema.
    """
    if isinstance(schema, dict):
        if "$ref" in schema:
            return resolve_ref(schema["$ref"], base_uri)

        for key, value in schema.items():
            schema[key] = resolve_nested_refs(value, base_uri)
    elif isinstance(schema, list):
        for i, item in enumerate(schema):
            schema[i] = resolve_nested_refs(item, base_uri)

    return schema


def check_property_descriptions(properties, base_uri, output, path=""):
    """
    Recursively check descriptions for all properties, including nested ones and arrays.
    """
    for prop_name, prop_details in properties.items():
        current_path = f"{path}.{prop_name}" if path else prop_name

        if "$ref" in prop_details:
            try:
                ref_schema = resolve_ref(prop_details["$ref"], base_uri)
                if "properties" in ref_schema:
                    check_property_descriptions(ref_schema["properties"], base_uri, output, current_path)
                if "description" in ref_schema:
                    description = ref_schema["description"]
                    is_valid, message = validate_description(description)
                    if not is_valid:
                        output.append(f"*** The attribute '{current_path}' has an invalid description: {message}")
                    else:
                        output.append(f"The attribute '{current_path}' is properly documented.")
                elif "properties" not in ref_schema:
                    output.append(f"*** The attribute '{current_path}' is missing a description.")
            except ValueError as e:
                output.append(f"*** Error resolving $ref for property '{current_path}': {e}")
        elif "properties" in prop_details:
            check_property_descriptions(prop_details["properties"], base_uri, output, current_path)
        elif "items" in prop_details:
            items = prop_details["items"]
            if "$ref" in items:
                try:
                    ref_schema = resolve_ref(items["$ref"], base_uri)
                    if "description" in ref_schema:
                        description = ref_schema["description"]
                        is_valid, message = validate_description(description)
                        if not is_valid:
                            output.append(f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                        else:
                            output.append(f"The attribute '{current_path}.items' is properly documented.")
                    else:
                        output.append(f"*** The attribute '{current_path}.items' is missing a description.")
                except ValueError as e:
                    output.append(f"*** Error resolving $ref for property '{current_path}.items': {e}")
            elif "anyOf" in items:
                for idx, any_of_item in enumerate(items["anyOf"]):
                    if "properties" in any_of_item:
                        check_property_descriptions(any_of_item["properties"], base_uri, output, f"{current_path}.items.anyOf[{idx}]")
                    elif "items" in any_of_item:
                        check_property_descriptions({"items": any_of_item["items"]}, base_uri, output, f"{current_path}.items.anyOf[{idx}]")
                    else:
                        if "description" not in any_of_item:
                            output.append(f"*** The attribute '{current_path}.items.anyOf[{idx}]' is missing a description.")
                        else:
                            description = any_of_item["description"]
                            is_valid, message = validate_description(description)
                            if not is_valid:
                                output.append(f"*** The attribute '{current_path}.items.anyOf[{idx}]' has an invalid description: {message}")
                            else:
                                output.append(f"The attribute '{current_path}.items.anyOf[{idx}]' is properly documented.")
            elif "properties" in items:
                check_property_descriptions(items["properties"], base_uri, output, f"{current_path}.items")
            elif "items" in items:
                check_property_descriptions({"items": items["items"]}, base_uri, output, current_path)
            else:
                if "description" not in items:
                    output.append(f"*** The attribute '{current_path}.items' is missing a description.")
                else:
                    description = items["description"]
                    is_valid, message = validate_description(description)
                    if not is_valid:
                        output.append(f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                    else:
                        output.append(f"The attribute '{current_path}.items' is properly documented.")
        elif "description" not in prop_details:
            output.append(f"*** The attribute '{current_path}' is missing a description.")
        else:
            description = prop_details["description"]
            is_valid, message = validate_description(description)
            if not is_valid:
                output.append(f"*** The attribute '{current_path}' has an invalid description: {message}")
            else:
                output.append(f"The attribute '{current_path}' is properly documented.")

def test_schema_descriptions(repo_to_test, options):
    """
    Test that all elements in the schema.json file include a description and that the description is valid.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if all descriptions are valid, False otherwise.
        output (list): List of messages describing the results of the test.
    """
    schema_file = join(repo_to_test, "schema.json")
    if not exists(schema_file):
        return "Checking that the schema is properly described in all its attributes", False, ["Schema file not found."]

    with open(schema_file, 'r') as f:
        schema = load(f)

    output = []
    base_uri = schema.get("$id", "")

    if "properties" in schema:
        check_property_descriptions(schema["properties"], base_uri, output)

    if "allOf" in schema:
        for item in schema["allOf"]:
            if "properties" in item:
                check_property_descriptions(item["properties"], base_uri, output)

    success = not any("invalid" in message or "missing" in message for message in output)

    test_name = "Checking that the schema is properly described in all its attributes"
    return test_name, success, output