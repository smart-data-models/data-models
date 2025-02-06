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

def find_duplicates_in_object(obj, path="", duplicates=None):
    """
    Recursively find duplicated attributes in a JSON object.

    Parameters:
        obj (dict): The JSON object to check.
        path (str): The current path in the JSON structure (used for reporting).
        duplicates (list): A list to store duplicate attribute paths.

    Returns:
        list: A list of duplicate attribute paths.
    """
    if duplicates is None:
        duplicates = []

    # Track attribute names at the current level
    attribute_counts = {}

    for key, value in obj.items():
        # Update the count for the current attribute
        if key in attribute_counts:
            attribute_counts[key] += 1
        else:
            attribute_counts[key] = 1

        # If the attribute is duplicated at this level, add it to the duplicates list
        if attribute_counts[key] > 1:
            duplicates.append(f"{path}.{key}" if path else key)

        # If the value is a dictionary, recursively check for duplicates
        if isinstance(value, dict):
            find_duplicates_in_object(value, f"{path}.{key}" if path else key, duplicates)

    return duplicates

def test_duplicated_attributes(repo_path):
    """
    Test if any attributes in the schema.json file are duplicated at the same object level.

    Parameters:
        repo_path (str): The path to the repository containing the schema.json file.

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking for duplicated attributes in schema.json"
    success = True
    output = []

    try:
        # Load the schema.json file
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        # Find duplicates in the schema
        duplicates = find_duplicates_in_object(schema)

        # Report duplicates
        if duplicates:
            success = False
            output.append("*** Duplicated attributes found:")
            for duplicate in duplicates:
                output.append(f"*** - {duplicate}")
        else:
            output.append("No duplicated attributes found.")

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output
#
# if __name__ == "__main__":
#     # Example usage
#     repo_path = "/path/to/repo"
#     test_name, success, output = test_duplicated_attributes(repo_path)
#     print(f"Test: {test_name}")
#     print(f"Success: {success}")
#     print("Output:")
#     for line in output:
#         print(line)
