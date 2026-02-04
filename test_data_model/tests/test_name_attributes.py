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
from jsonpointer import resolve_pointer
from .utils import resolve_ref, resolve_ref_with_url

def check_attribute_case(properties, base_uri, output, repo_files, path="", processed_refs=None):
    """
    Recursively check attribute names for starting with capital letters.
    Keeps track of processed references to avoid duplicate processing.
    """
    if processed_refs is None:
        processed_refs = set()

    for key, prop_details in properties.items():
        current_path = f"{path}.{key}" if path else key
        
        # Skip special attributes like @context, id, type
        if key.startswith("@") or key in ["id", "type"]:
            pass
        elif key[0].isupper():
            output.append(f"*** The attribute '{current_path}' starts with a capital letter. Please use camelCase.")
        
        # Check $ref
        if "$ref" in prop_details:
            ref = prop_details["$ref"]
            
            # Create a unique identifier for the ref to avoid cycles/duplicates
            # Using tuple of (base_uri, ref)
            ref_id = (base_uri, ref)
            
            if ref_id in processed_refs:
                continue
            processed_refs.add(ref_id)
            
            try:
                ref_schema, resolved_url = resolve_ref_with_url(repo_files, ref, base_uri)
                if "properties" in ref_schema:
                    check_attribute_case(ref_schema["properties"], resolved_url, output, repo_files, current_path, processed_refs)
            except ValueError as e:
                output.append(f"*** Error resolving $ref for property '{current_path}': {e}")
            continue

        # Check nested properties (for objects)
        if "properties" in prop_details:
            check_attribute_case(prop_details["properties"], base_uri, output, repo_files, current_path, processed_refs)

        # Check items (for arrays)
        if "items" in prop_details:
            items = prop_details["items"]
            if isinstance(items, list):
                # Tuple validation
                for idx, item in enumerate(items):
                     if "properties" in item:
                         check_attribute_case(item["properties"], base_uri, output, repo_files, f"{current_path}.items[{idx}]", processed_refs)
            elif isinstance(items, dict):
                # List validation
                # Check for $ref in items
                if "$ref" in items:
                    try:
                        items_ref = items["$ref"]
                        items_ref_id = (base_uri, items_ref)
                        
                        if items_ref_id not in processed_refs:
                            processed_refs.add(items_ref_id)
                            ref_schema, resolved_url = resolve_ref_with_url(repo_files, items_ref, base_uri)
                            
                            if "properties" in ref_schema:
                                check_attribute_case(ref_schema["properties"], resolved_url, output, repo_files,
                                                     f"{current_path}.items", processed_refs)
                    except ValueError as e:
                        output.append(f"*** Error resolving $ref for items in '{current_path}': {e}")
            elif "anyOf" in items:
                for idx, any_of_item in enumerate(items["anyOf"]):
                    if "properties" in any_of_item:
                        check_attribute_case(any_of_item["properties"], base_uri, output, repo_files,
                                             f"{current_path}.items.anyOf[{idx}]", processed_refs)
            elif "properties" in items:
                check_attribute_case(items["properties"], base_uri, output, repo_files,
                                     f"{current_path}.items", processed_refs)
            elif "items" in items:
                check_attribute_case({"items": items["items"]}, base_uri, output, repo_files,
                                     current_path, processed_refs)


def test_name_attributes(repo_files, options):
    """
    Test that no attribute names start with capital letters.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if no attributes start with capital letters, False otherwise.
        output (list): List of warning messages if any attributes start with capital letters.
    """
    file_name = "schema.json"
    test_name = "Checking attribute naming conventions (camelCase)"

    if file_name not in repo_files or repo_files[file_name] is None:
        return test_name, False, ["Schema file not found."]

    file_data = repo_files[file_name]
    if "json" not in file_data:
        return test_name, False, [f"Invalid JSON: {file_data.get('json_error', 'Unknown error')}"]

    schema = file_data["json"]

    output = []
    base_uri = schema.get("$id", "")

    if "properties" in schema:
        check_attribute_case(schema["properties"], base_uri, output, repo_files)

    if "allOf" in schema:
        for idx, item in enumerate(schema["allOf"]):
            if "$ref" in item:
                try:
                    ref_schema, resolved_url = resolve_ref_with_url(repo_files, item["$ref"], base_uri)
                    if "properties" in ref_schema:
                        check_attribute_case(ref_schema["properties"], resolved_url, output, repo_files, f"allOf[{idx}]")
                except ValueError as e:
                    output.append(f"*** Error resolving $ref in allOf[{idx}]: {e}")
            elif "properties" in item:
                check_attribute_case(item["properties"], base_uri, output, repo_files, f"allOf[{idx}]")

    # Filter out duplicate messages
    unique_output = []
    seen_messages = set()
    for message in output:
        if message not in seen_messages:
            unique_output.append(message)
            seen_messages.add(message)

    # Determine success (warnings might be okay depending on policy, but usually test fails on error)
    # The previous code seemed to fail on capitals
    # But we'll return False if there are any errors (like schema not found)
    success = not any(message.startswith("***") for message in unique_output)

    return test_name, success, unique_output
