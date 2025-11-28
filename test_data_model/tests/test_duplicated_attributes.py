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
# version 23/09/25 - 2
import json
import os
import jsonref
import urllib.request
import urllib.parse


def extract_attributes_from_payload(payload, parent_path=""):
    """
    Recursively extract all attributes from a JSON payload, including their full paths.
    """
    attributes = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            full_path = f"{parent_path}.{key}" if parent_path else key
            attributes.add(full_path)
            attributes.update(extract_attributes_from_payload(value, full_path))
    elif isinstance(payload, list):
        for item in payload:
            attributes.update(extract_attributes_from_payload(item, parent_path))
    return attributes


def extract_attributes_from_schema(schema, parent_path="", base_uri=""):
    """
    Recursively extract all attributes defined in a JSON schema, including their full paths.
    Handles $ref references properly by fully resolving them.
    """
    attributes = set()

    # If schema is already a reference that's been resolved by jsonref
    # it might be a proxy object with additional attributes
    schema_dict = dict(schema) if hasattr(schema, '__getitem__') else schema

    # Handle properties
    if "properties" in schema_dict:
        for key, value in schema_dict["properties"].items():
            full_path = f"{parent_path}.{key}" if parent_path else key
            attributes.add(full_path)
            if isinstance(value, dict) or hasattr(value, '__getitem__'):
                attributes.update(extract_attributes_from_schema(value, full_path, base_uri))

    # Handle nested arrays
    if "items" in schema_dict:
        if isinstance(schema_dict["items"], dict) or hasattr(schema_dict["items"], '__getitem__'):
            attributes.update(extract_attributes_from_schema(schema_dict["items"], parent_path, base_uri))
        elif isinstance(schema_dict["items"], list):
            for item in schema_dict["items"]:
                if isinstance(item, dict) or hasattr(item, '__getitem__'):
                    attributes.update(extract_attributes_from_schema(item, parent_path, base_uri))

    # Handle allOf, anyOf, oneOf
    for combiner in ["allOf", "anyOf", "oneOf"]:
        if combiner in schema_dict:
            for item in schema_dict[combiner]:
                attributes.update(extract_attributes_from_schema(item, parent_path, base_uri))

    # Handle additionalProperties if it's an object schema
    if "additionalProperties" in schema_dict and isinstance(schema_dict["additionalProperties"], dict):
        attributes.update(extract_attributes_from_schema(schema_dict["additionalProperties"], parent_path, base_uri))

    # removing languageMap for languageMap properties
    filtered_attributes = [item.replace('.languageMap', '') for item in attributes]

    return filtered_attributes


def test_duplicated_attributes(repo_files, options):
    """
    Test that all attributes in the JSON payload are defined in the schema.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if all attributes are defined, False otherwise.
        output (list): List of messages describing the results of the test.
    """
    test_name = "Checking that all payload attributes are defined in the schema"
    
    schema_file = "schema.json"
    payload_file = "examples/example.json"

    if schema_file not in repo_files or repo_files[schema_file] is None:
        return test_name, False, ["Schema file not found."]
    if payload_file not in repo_files or repo_files[payload_file] is None:
        return test_name, False, ["Payload file not found."]

    schema_data = repo_files[schema_file]
    if "json" not in schema_data:
        return test_name, False, ["Schema file is not a valid JSON."]
    
    payload_data = repo_files[payload_file]
    if "json" not in payload_data:
        return test_name, False, ["Payload file is not a valid JSON."]

    # Normalize the base URI to ensure proper resolution of references
    # Use the path from repo_files if available
    if "path" in schema_data and schema_data["path"]:
        schema_dir = os.path.dirname(os.path.abspath(schema_data["path"]))
        base_uri = urllib.parse.urljoin('file:', urllib.request.pathname2url(schema_dir))
    else:
        # Fallback if path is not available (should be present)
        base_uri = ""

    # Load the schema and fully resolve all $ref references using jsonref
    # We use jsonref.loads on the content string, which should be available
    try:
        schema = jsonref.loads(
            schema_data["content"],
            base_uri=base_uri,
            lazy_load=False,
            load_on_repr=True
        )
    except Exception as e:
        return test_name, False, [f"Error parsing/resolving schema: {e}"]

    payload = payload_data["json"]

    output = []

    # Extract attributes from the payload and schema
    payload_attributes = extract_attributes_from_payload(payload)
    schema_attributes = extract_attributes_from_schema(schema, base_uri=base_uri)

    # Debug information if needed
    output.append(f"Schema attributes: {sorted(schema_attributes)}")
    output.append(f"Payload attributes: {sorted(payload_attributes)}")

    # Check for attributes in the payload that are not in the schema
    undefined_attributes = []
    for attribute in payload_attributes:
        if attribute not in schema_attributes:
            undefined_attributes.append(attribute)

    if undefined_attributes:
        output.append("The following attributes in the payload are not defined in the schema:")
        for attribute in sorted(undefined_attributes):
            output.append(f"*** Attribute '{attribute}' in the payload is not defined in the schema.")

    # Determine if the test was successful
    success = len(undefined_attributes) == 0

    return test_name, success, output
