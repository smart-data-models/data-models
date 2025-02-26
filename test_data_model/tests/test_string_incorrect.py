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

def test_string_incorrect(repo_path, options):
    """
    Validate that attributes with type 'string' do not have 'items' or 'properties'.

    Parameters:
        repo_path (str): The path to the schema.json file.

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking invalid string attributes"
    success = True
    output = []

#    Example usage of the options parameter (optional, for future flexibility)
#    if options.get("published", False):
#        unpublished = True
#    if options.get("private", False):
#        output.append("This is a private model.")

    try:
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        def validate_properties(properties, path=""):
            nonlocal success
            for key, value in properties.items():
                if isinstance(value, dict):
                    type_value = value.get("type", "")
                    if type_value == "string" and ("items" in value or "properties" in value):
                        success = False
                        output.append(f"*** Error: Attribute '{path + key}' is of type 'string' but has invalid subelements ('items' or 'properties').")

                    # Recursively check nested properties
                    if "properties" in value and isinstance(value["properties"], dict):
                        validate_properties(value["properties"], path + key + ".")

        if "properties" in schema and isinstance(schema["properties"], dict):
            validate_properties(schema["properties"])

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output

# Example of calling the function
#repo_path = "your_repo_path_here"
#test_name, success, results = check_invalid_string_attributes(repo_path)
#print(test_name)
#for line in results:
#    print(line)

