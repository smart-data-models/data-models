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

import os
import yaml

def validate_yaml_file(file_path):
    """
    Validate that a YAML file is properly formatted.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        tuple: (success, message)
            success (bool): True if the YAML file is valid, False otherwise.
            message (str): A message describing the result of the validation.
    """
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        # Extract only the filename from the full path
        file_name = os.path.basename(file_path)
        return True, f"The file '{file_name}' is a valid YAML file."
    except yaml.YAMLError as e:
        # Extract only the filename from the full path
        file_name = os.path.basename(file_path)
        return False, f"*** The file '{file_name}' is not a valid YAML file: {e}"
    except Exception as e:
        # Extract only the filename from the full path
        file_name = os.path.basename(file_path)
        return False, f"*** An error occurred while reading '{file_name}': {e}"

def test_yaml_files(repo_to_test, options):
    """
    Test that the ADOPTERS.yaml and notes.yaml files are valid YAML files.

    Parameters:
        repo_to_test (str): The path to the directory where the files are located.

    Returns:
        tuple: (test_name, success, output)
            test_name (str): Name of the test.
            success (bool): True if both files are valid YAML, False otherwise.
            output (list): List of messages describing the results of the test.
    """
    # List of YAML files to validate
    yaml_files = ["ADOPTERS.yaml", "notes.yaml"]
    output = []
    success = True

#    Example usage of the options parameter (optional, for future flexibility)
#    if options.get("published", False):
#        unpublished = True
#    if options.get("private", False):
#        output.append("This is a private model.")


    for yaml_file in yaml_files:
        file_path = os.path.join(repo_to_test, yaml_file)
        if not os.path.exists(file_path):
            output.append(f"*** The file '{yaml_file}' does not exist.")
            success = False
        else:
            is_valid, message = validate_yaml_file(file_path)
            output.append(message)
            if not is_valid:
                success = False

    test_name = "Checking that ADOPTERS.yaml and notes.yaml are valid YAML files"
    return test_name, success, output
