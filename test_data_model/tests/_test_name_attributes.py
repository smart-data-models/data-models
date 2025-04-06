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
#  Author: Your Name                                                            #
#################################################################################

import json
import os
from urllib.parse import urljoin
import requests
from jsonpointer import resolve_pointer

def check_attribute_case(properties, base_uri, output, path="", processed_refs=None):
    """
    Recursively check attribute names for starting with capital letters.
    Keeps track of processed references to avoid duplicate processing.
    """
    if processed_refs is None:
        processed_refs = set()

    for prop_name, prop_details in properties.items():
        current_path = f"{path}.{prop_name}" if path else prop_name

        # Check if attribute name starts with capital letter
        if prop_name[0].isupper():
            output.append(f"Warning: The attribute '{current_path}' starts with a capital letter - it's recommended to use camelCase for attribute names.")

        # Handle $ref properties
        if "$ref" in prop_details:
            ref = prop_details["$ref"]
            ref_id = f"{current_path}:{ref}"

            if ref_id in processed_refs:
                continue

            processed_refs.add(ref_id)

            try:
                ref_schema = resolve_ref(ref, base_uri)
                if "properties" in ref_schema:
                    check_attribute_case(ref_schema["properties"], base_uri, output, current_path, processed_refs)
            except ValueError as e:
                output.append(f"*** Error resolving $ref for property '{current_path}': {e}")
            continue

        # Check nested properties (for objects)
        if "properties" in prop_details:
            check_attribute_case(prop_details["properties"], base_uri, output, current_path, processed_refs)

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

                        if "properties" in ref_schema:
                            check_attribute_case(ref_schema["properties"], base_uri, output,
                                               f"{current_path}.items", processed_refs)
                except ValueError as e:
                    output.append(f"*** Error resolving $ref for items in '{current_path}': {e}")
            elif "anyOf" in items:
                for idx, any_of_item in enumerate(items["anyOf"]):
                    if "properties" in any_of_item:
                        check_attribute_case(any_of_item["properties"], base_uri, output,
                                           f"{current_path}.items.anyOf[{idx}]", processed_refs)
            elif "properties" in items:
                check_attribute_case(items["properties"], base_uri, output,
                                   f"{current_path}.items", processed_refs)
            elif "items" in items:
                check_attribute_case({"items": items["items"]}, base_uri, output,
                                   current_path, processed_refs)

def resolve_ref(ref, base_uri):
    """
    Resolve a $ref to its external schema (same as in the original file).
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
            schema = resolve_pointer(schema, pointer_part)
        except Exception as e:
            raise ValueError(f"*** Failed to resolve JSON Pointer '{pointer_part}' in schema: {e}")

    return schema

def test_name_attributes(repo_to_test, options):
    """
    Test that no attribute names start with capital letters.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if no attributes start with capital letters, False otherwise.
        output (list): List of warning messages if any attributes start with capital letters.
    """
    schema_file = os.path.join(repo_to_test, "schema.json")
    if not os.path.exists(schema_file):
        return "Checking attribute naming conventions (camelCase)", False, ["Schema file not found."]

    with open(schema_file, 'r') as f:
        schema = json.load(f)

    output = []
    base_uri = schema.get("$id", "")

    if "properties" in schema:
        check_attribute_case(schema["properties"], base_uri, output)

    if "allOf" in schema:
        for idx, item in enumerate(schema["allOf"]):
            if "$ref" in item:
                try:
                    ref_schema = resolve_ref(item["$ref"], base_uri)
                    if "properties" in ref_schema:
                        check_attribute_case(ref_schema["properties"], base_uri, output, f"allOf[{idx}]")
                except ValueError as e:
                    output.append(f"*** Error resolving $ref in allOf[{idx}]: {e}")
            elif "properties" in item:
                check_attribute_case(item["properties"], base_uri, output, f"allOf[{idx}]")

    # Filter out duplicate messages
    output = []
    seen = set()
    for message in output:
        if message not in seen:
            seen.add(message)
            output.append(message)

    # This test is considered successful even if there are warnings (they're just recommendations)
    # But we'll return False if there are any errors (like schema not found)
    success = not any(message.startswith("***") for message in output)

    test_name = "Checking attribute naming conventions (camelCase)"
    return test_name, success, output