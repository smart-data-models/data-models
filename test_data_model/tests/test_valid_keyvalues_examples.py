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
from jsonschema import validate, ValidationError

def validate_json_against_schema(json_data, schema):
    """
    Validate JSON data against a JSON schema.

    Parameters:
        json_data (dict): The JSON data to validate.
        schema (dict): The JSON schema to validate against.

    Returns:
        tuple: (success, message)
            success (bool): True if the JSON data is valid, False otherwise.
            message (str): A message describing the result of the validation.
    """
    try:
        validate(instance=json_data, schema=schema)
        return True, "JSON data is valid against the schema."
    except ValidationError as e:
        return False, f"*** JSON data is not valid against the schema: {e}"

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
                    warnings.append(f"*** The @context URL '{url}' does not return a valid response (HTTP {response.status_code}).")
            except Exception as e:
                warnings.append(f"*** The @context URL '{url}' is not reachable: {e}")

        if warnings:
            return False, "WARNING: " + " ".join(warnings) + " Ignore this if it is an unpublished data model."
        else:
            return True, "All @context URLs are valid."
    else:
        return False, "*** Invalid @context format. Expected a URL or an array of URLs."

def test_valid_keyvalues_examples(repo_to_test, options):
    """
    Test that the example.json and example.jsonld files are valid against the schema.json file.
    Also, check that the @context URL(s) in example.jsonld are valid (report a warning if any are not reachable).

    Parameters:
        repo_to_test (str): The path to the directory where the files are located.

    Returns:
        tuple: (test_name, success, output)
            test_name (str): Name of the test.
            success (bool): True if both files are valid, False otherwise.
            output (list): List of messages describing the results of the test.
    """
    # Paths to the files
    schema_file = os.path.join(repo_to_test, "schema.json")
    example_json_file = os.path.join(repo_to_test, "examples", "example.json")
    example_jsonld_file = os.path.join(repo_to_test, "examples", "example.jsonld")

    output = []
    success = True

#    Example usage of the options parameter (optional, for future flexibility)
#    if options.get("published", False):
#        unpublished = True
#    if options.get("private", False):
#        output.append("This is a private model.")


    # Check if the schema file exists
    if not os.path.exists(schema_file):
        return "Checking that example files are valid against the schema", False, ["Schema file not found."]

    # Load the schema
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    # Validate example.json
    if os.path.exists(example_json_file):
        with open(example_json_file, 'r') as f:
            example_json = json.load(f)
        is_valid, message = validate_json_against_schema(example_json, schema)
        output.append(f"example.json: {message}")
        if not is_valid:
            success = False
    else:
        output.append("*** example.json file not found.")
        success = False

    # Validate example.jsonld
    if os.path.exists(example_jsonld_file):
        with open(example_jsonld_file, 'r') as f:
            example_jsonld = json.load(f)
        is_valid, message = validate_json_against_schema(example_jsonld, schema)
        output.append(f"example.jsonld: {message}")
        if not is_valid:
            success = False

        # Check the @context URL(s) in example.jsonld
        if "@context" in example_jsonld:
            context = example_jsonld["@context"]
            is_context_valid, context_message = check_context_url(context)
            if not is_context_valid:
                output.append(context_message)  # Warning message
            else:
                output.append(context_message)
        else:
            output.append("*** example.jsonld is missing the mandatory '@context' attribute.")
            success = False
    else:
        output.append("*** example.jsonld file not found.")
        success = False

    test_name = "Checking that example files are valid against the schema"
    return test_name, success, output

# Example usage (for standalone testing)
# if __name__ == "__main__":
#     repo_to_test = "path/to/repo"  # Replace with the actual path to the repository
#     test_name, success, output = test_valid_keyvalues_examples(repo_to_test)
#     print(f"Test Name: {test_name}")
#     print(f"Success: {success}")
#     print("Output:")
#     for message in output:
#         print(message) 
