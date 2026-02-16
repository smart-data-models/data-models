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
import re
from .utils import resolve_ref, resolve_ref_with_url

def validate_description(description):
    """
    Validate the format of the description field.
    The expected format is: "Property/Relationship/Geoproperty. <Description>. Model:'<Model>'. [Enum:'<Enum>']. [Units:'<Units>']."
    """
    if not isinstance(description, str):
        return False, "Description must be a string."

    # Split the description into parts
    parts = description.split(". ")
    
    # 1. Check the first part (Property/Relationship/Geoproperty)
    valid_types = ["Property", "Relationship", "Geoproperty"]
    if parts[0] not in valid_types:
        return False, f"Invalid type '{parts[0]}'. Expected one of {valid_types}."

    # 2. Check for Model (mandatory)
    # model_pattern = re.compile(r"Model:'[^']+'")
    # if not any(model_pattern.search(part) for part in parts):
    #     return False, "Missing 'Model:' definition."

    # 3. Check for Enum (optional, but must be valid if present)
    enum_pattern = re.compile(r"Enum:'[^']+'")
    # Check if any part looks like an Enum definition but is malformed
    for part in parts:
        if "Enum:" in part:
            if not enum_pattern.search(part):
                 return False, f"Invalid format for 'Enum:'. Expected format: Enum:'value'."

    # 4. Check for Units (optional, but must be valid if present)
    units_pattern = re.compile(r"Units:'[^']+'")
    for part in parts:
        if "Units:" in part:
             if not units_pattern.search(part):
                 return False, f"Invalid format for 'Units:'. Expected format: Units:'value'."

    return True, "Description is valid."

def check_property_descriptions(properties, base_uri, output, repo_files, path="", processed_refs=None, is_external_ref=False, recursion_depth=0):
    """
    Recursively check descriptions for all properties, including nested ones and arrays.
    Keeps track of processed references to avoid duplicate processing.
    For properties in external referenced schemas, only checks for presence of description,
    not the detailed format (to maintain backward compatibility with common schemas).
    """
    if processed_refs is None:
        processed_refs = set()

    for key, prop_details in properties.items():
        current_path = f"{path}.{key}" if path else key

        # Check if this is a property with $ref
        has_ref = "$ref" in prop_details

        # Check if description exists - but use different validation for external vs local schemas
        if "description" in prop_details:
            if is_external_ref or has_ref:
                # For properties from external referenced schemas, don't validate the detailed format
                # For local $ref properties, also skip format validation for consistency
                output.append(f"The attribute '{current_path}' is properly documented.")
            else:
                # For local properties in the main schema, validate the detailed format
                is_valid, message = validate_description(prop_details["description"])
                if is_valid:
                    output.append(f"The attribute '{current_path}' is properly documented.")
                else:
                    output.append(f"*** The attribute '{current_path}' has an invalid description: {message}")
        else:
            # Check if it's a $ref, in which case the description might be in the referenced schema
            if not has_ref:
                 output.append(f"*** The attribute '{current_path}' is missing a description.")

        # Check $ref
        if has_ref:
            # Check recursion limit
            if recursion_depth > 4:
                continue

            ref = prop_details["$ref"]
            ref_id = (base_uri, ref)

            if ref_id in processed_refs:
                continue
            processed_refs.add(ref_id)

            try:
                ref_schema, resolved_url = resolve_ref_with_url(repo_files, ref, base_uri)
                if "properties" in ref_schema:
                    # Properties in external referenced schemas don't need strict format validation
                    check_property_descriptions(ref_schema["properties"], resolved_url, output, repo_files, current_path,
                                                processed_refs, is_external_ref=True, recursion_depth=recursion_depth + 1)
                if "description" in ref_schema:
                    # For referenced schemas, only check existence, not format validation
                    output.append(f"The attribute '{current_path}' is properly documented.")

            except ValueError as e:
                output.append(f"*** Error resolving $ref for property '{current_path}': {e}")
            continue

        # Check nested properties (for objects)
        if "properties" in prop_details:
            check_property_descriptions(prop_details["properties"], base_uri, output, repo_files, current_path, processed_refs, is_external_ref, recursion_depth)

        # Check items (for arrays)
        if "items" in prop_details:
            items = prop_details["items"]
            if isinstance(items, list):
                # Tuple validation
                for idx, item in enumerate(items):
                    if "properties" in item:
                        check_property_descriptions(item["properties"], base_uri, output, repo_files, f"{current_path}.items[{idx}]", processed_refs, is_external_ref, recursion_depth)
            elif isinstance(items, dict):
                # List validation
                # Check for $ref in items
                if "$ref" in items:
                    # Check recursion limit
                    if recursion_depth > 4:
                        continue
                    
                    items_ref = items["$ref"]
                    items_ref_id = (base_uri, items_ref)
                    
                    if items_ref_id not in processed_refs:
                        processed_refs.add(items_ref_id)
                        try:
                            ref_schema, resolved_url = resolve_ref_with_url(repo_files, items_ref, base_uri)
                            
                            if "description" in ref_schema:
                                description = ref_schema["description"]
                                is_valid, message = validate_description(description)
                                if is_valid:
                                    output.append(f"The attribute '{current_path}.items' is properly documented.")
                                else:
                                    output.append(f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                            else:
                                output.append(f"*** The attribute '{current_path}.items' is missing a description.")

                            if "properties" in ref_schema:
                                check_property_descriptions(ref_schema["properties"], resolved_url, output, repo_files,
                                                            f"{current_path}.items", processed_refs, is_external_ref, recursion_depth=recursion_depth + 1)
                        except ValueError as e:
                             output.append(f"*** Error resolving $ref for items in '{current_path}': {e}")
                elif "anyOf" in items:
                    for idx, any_of_item in enumerate(items["anyOf"]):
                        if "properties" in any_of_item:
                            check_property_descriptions(any_of_item["properties"], base_uri, output, repo_files,
                                                        f"{current_path}.items.anyOf[{idx}]", processed_refs, is_external_ref, recursion_depth)
                        elif "items" in any_of_item:
                            nested_items_path = f"{current_path}.items.anyOf[{idx}]"
                            if "description" not in any_of_item:
                                output.append(f"*** The attribute '{nested_items_path}' is missing a description.")
                            check_property_descriptions({"items": any_of_item["items"]}, base_uri, output, repo_files,
                                                        nested_items_path, processed_refs, is_external_ref, recursion_depth)
                        else:
                            if is_external_ref:
                                if "description" in any_of_item:
                                    output.append(f"The attribute '{current_path}.items.anyOf[{idx}]' is properly documented.")
                                else:
                                    output.append(f"*** The attribute '{current_path}.items.anyOf[{idx}]' is missing a description.")
                            else:
                                if "description" not in any_of_item:
                                    output.append(f"*** The attribute '{current_path}.items.anyOf[{idx}]' is missing a description.")
                                else:
                                    is_valid, message = validate_description(any_of_item["description"])
                                    if not is_valid:
                                        output.append(
                                            f"*** The attribute '{current_path}.items.anyOf[{idx}]' has an invalid description: {message}")
                                    else:
                                        output.append(
                                            f"The attribute '{current_path}.items.anyOf[{idx}]' is properly documented.")
                elif "properties" in items:
                    check_property_descriptions(items["properties"], base_uri, output, repo_files, f"{current_path}.items",
                                                processed_refs, is_external_ref, recursion_depth)
                elif "items" in items:
                    check_property_descriptions({"items": items["items"]}, base_uri, output, repo_files, current_path, processed_refs, is_external_ref, recursion_depth)
                else:
                    if "description" not in items:
                        output.append(f"*** The attribute '{current_path}.items' is missing a description.")
                    else:
                        is_valid, message = validate_description(items["description"])
                        if not is_valid:
                            output.append(f"*** The attribute '{current_path}.items' has an invalid description: {message}")
                        else:
                            output.append(f"The attribute '{current_path}.items' is properly documented.")


def test_schema_descriptions(repo_files, options):
    """
    Test that all elements in the schema.json file include a description and that the description is valid.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if all descriptions are valid, False otherwise.
        output (list): List of messages describing the results of the test.
    """
    file_name = "schema.json"
    test_name = "Checking that the schema is properly described in all its attributes"

    if file_name not in repo_files or repo_files[file_name] is None:
        return test_name, False, ["Schema file not found."]

    file_data = repo_files[file_name]
    if "json" not in file_data:
        return test_name, False, ["Schema file is not a valid JSON"]

    schema = file_data["json"]

    output = []
    base_uri = schema.get("$id", "")

    # Check root description
    if "description" not in schema:
        output.append("*** The schema is missing a root description.")
    else:
        output.append("The schema has a root description.")

    if "properties" in schema:
        check_property_descriptions(schema["properties"], base_uri, output, repo_files, is_external_ref=False)

    if "allOf" in schema:
        for idx, item in enumerate(schema["allOf"]):
            if "$ref" in item:
                try:
                    ref_schema, resolved_url = resolve_ref_with_url(repo_files, item["$ref"], base_uri)
                    if "properties" in ref_schema:
                        # Properties from external schemas (common schemas) don't need strict format validation
                        check_property_descriptions(ref_schema["properties"], resolved_url, output, repo_files, f"allOf[{idx}]", is_external_ref=True, recursion_depth=1)
                except ValueError as e:
                    output.append(f"*** Error resolving $ref in allOf[{idx}]: {e}")
            elif "properties" in item:
                check_property_descriptions(item["properties"], base_uri, output, repo_files, f"allOf[{idx}]")

    # Filter out duplicate messages
    unique_output = []
    seen_messages = set()
    for message in output:
        if message not in seen_messages:
            unique_output.append(message)
            seen_messages.add(message)

    success = not any("invalid" in message or "missing" in message or "***" in message for message in unique_output)

    return test_name, success, unique_output
