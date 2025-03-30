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
# version 28/02/25 - 1
import json
import os
import requests
from urllib.parse import urljoin
from jsonpointer import resolve_pointer


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

    parts = [part for part in description.split(". ")]

    valid_ngsi_types = ["Property", "GeoProperty", "Relationship", "LanguageProperty", "ListProperty"]
    ngsi_type_found = None
    for part in parts:
        if part in valid_ngsi_types:
            ngsi_type_found = part
            break

    if not ngsi_type_found:
        for part in parts:
            for ngsi_type in valid_ngsi_types:
                if ngsi_type in part and part != ngsi_type:
                    return False, f"NGSI type '{part}' contains extra characters."
        return False, "*** NGSI type is not described. Must be one of: Property, GeoProperty, Relationship, LanguageProperty, ListProperty"

    if ngsi_type_found.strip() != ngsi_type_found:
        return False, f"*** NGSI type '{ngsi_type_found}' contains extra spaces."

    optional_keys = ["Model:", "Units:", "Enum:", "Privacy:", "Multilingual"]
    for part in parts:
        for key in optional_keys:
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
    if "#" in ref:
        url_part, pointer_part = ref.split("#", 1)
    else:
        url_part, pointer_part = ref, ""

    if url_part.startswith("http"):
        resolved_url = url_part
    else:
        resolved_url = urljoin(base_uri, url_part)

    response = requests.get(resolved_url)
    if response.status_code != 200:
        raise ValueError(f"*** Failed to fetch external schema from {resolved_url}")

    schema = response.json()

    if pointer_part:
        try:
            # Resolve the JSON Pointer relative to the fetched schema
            schema = resolve_pointer(schema, pointer_part)
        except Exception as e:
            raise ValueError(f"*** Failed to resolve JSON Pointer '{pointer_part}' in schema: {e}")

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
        else:
            for key, value in schema.items():
                schema[key] = resolve_nested_refs(value, base_uri)
    elif isinstance(schema, list):
        for i, item in enumerate(schema):
            schema[i] = resolve_nested_refs(item, base_uri)

    return schema


def check_property_descriptions(properties, base_uri, output, path="", processed_refs=None):
    """
    Recursively check descriptions for all properties, including nested ones and arrays.
    Keeps track of processed references to avoid duplicate processing.
    """
    if processed_refs is None:
        processed_refs = set()

    for prop_name, prop_details in properties.items():
        current_path = f"{path}.{prop_name}" if path else prop_name

        # Handle $ref properties
        if "$ref" in prop_details:
            ref = prop_details["$ref"]
            ref_id = f"{current_path}:{ref}"

            # Skip if this reference has already been processed for this path
            if ref_id in processed_refs:
                continue

            processed_refs.add(ref_id)

            try:
                ref_schema = resolve_ref(ref, base_uri)
                if "properties" in ref_schema:
                    check_property_descriptions(ref_schema["properties"], base_uri, output, current_path,
                                                processed_refs)
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
            continue

        # Check description for the current property
        if "description" not in prop_details:
            # Only report missing description if it's not a container that will have its items checked separately
            if not ("properties" in prop_details or "items" in prop_details):
                output.append(f"*** The attribute '{current_path}' is missing a description.")
            else:
                # For arrays and objects, explicitly note that the container itself needs a description
                if "properties" in prop_details:
                    output.append(f"*** The attribute '{current_path}' (object) is missing a description.")
                elif "items" in prop_details:
                    output.append(f"*** The attribute '{current_path}' (array) is missing a description.")
        else:
            description = prop_details["description"]
            is_valid, message = validate_description(description)
            if not is_valid:
                output.append(f"*** The attribute '{current_path}' has an invalid description: {message}")
            else:
                output.append(f"The attribute '{current_path}' is properly documented.")

        # Check nested properties (for objects)
        if "properties" in prop_details:
            check_property_descriptions(prop_details["properties"], base_uri, output, current_path, processed_refs)

        # Check items (for arrays)
        if "items" in prop_details:
            items = prop_details["items"]

            if "$ref" in items:
                try:
                    items_ref = items["$ref"]
                    items_ref_id = f"{current_path}.items:{items_ref}"

                    if items_ref_id not in processed_refs:
                        processed_refs.add(items_ref_id)
                        ref_schema = resolve_ref(items_ref, base_uri)

                        if "description" in ref_schema:
                            description = ref_schema["description"]
                            is_valid, message = validate_description(description)
                            if not is_valid:
                                output.append(
                                    f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                            else:
                                output.append(f"The attribute '{current_path}.items' is properly documented.")
                        else:
                            output.append(f"*** The attribute '{current_path}.items' is missing a description.")

                        if "properties" in ref_schema:
                            check_property_descriptions(ref_schema["properties"], base_uri, output,
                                                        f"{current_path}.items", processed_refs)
                except ValueError as e:
                    output.append(f"*** Error resolving $ref for items in '{current_path}': {e}")
            elif "anyOf" in items:
                for idx, any_of_item in enumerate(items["anyOf"]):
                    if "properties" in any_of_item:
                        check_property_descriptions(any_of_item["properties"], base_uri, output,
                                                    f"{current_path}.items.anyOf[{idx}]", processed_refs)
                    elif "items" in any_of_item:
                        nested_items_path = f"{current_path}.items.anyOf[{idx}]"
                        if "description" not in any_of_item:
                            output.append(f"*** The attribute '{nested_items_path}' is missing a description.")
                        check_property_descriptions({"items": any_of_item["items"]}, base_uri, output,
                                                    nested_items_path, processed_refs)
                    else:
                        if "description" not in any_of_item:
                            output.append(
                                f"*** The attribute '{current_path}.items.anyOf[{idx}]' is missing a description.")
                        else:
                            description = any_of_item["description"]
                            is_valid, message = validate_description(description)
                            if not is_valid:
                                output.append(
                                    f"*** The attribute '{current_path}.items.anyOf[{idx}]' has an invalid description: {message}")
                            else:
                                output.append(
                                    f"The attribute '{current_path}.items.anyOf[{idx}]' is properly documented.")
            elif "properties" in items:
                check_property_descriptions(items["properties"], base_uri, output, f"{current_path}.items",
                                            processed_refs)
            elif "items" in items:
                check_property_descriptions({"items": items["items"]}, base_uri, output, current_path, processed_refs)
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


def test_schema_descriptions(repo_to_test, options):
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
    base_uri = schema.get("$id", "")

    # Check the schema description itself - but don't validate it with the NGSI requirements
    if "description" not in schema:
        output.append("*** The schema is missing a root description.")
    else:
        # For the root schema, we only check that a description exists, not its format
        output.append("The schema has a root description.")

    if "properties" in schema:
        check_property_descriptions(schema["properties"], base_uri, output)

    if "allOf" in schema:
        for idx, item in enumerate(schema["allOf"]):
            if "$ref" in item:
                try:
                    ref_schema = resolve_ref(item["$ref"], base_uri)
                    if "properties" in ref_schema:
                        check_property_descriptions(ref_schema["properties"], base_uri, output, f"allOf[{idx}]")
                except ValueError as e:
                    output.append(f"*** Error resolving $ref in allOf[{idx}]: {e}")
            elif "properties" in item:
                check_property_descriptions(item["properties"], base_uri, output, f"allOf[{idx}]")

    # Filter out duplicate messages
    unique_output = []
    seen = set()
    for message in output:
        if message not in seen:
            seen.add(message)
            unique_output.append(message)

    success = not any("invalid" in message or "missing" in message for message in unique_output)

    test_name = "Checking that the schema is properly described in all its attributes"
    return test_name, success, unique_output