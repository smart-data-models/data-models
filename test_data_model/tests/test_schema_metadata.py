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
import re
import requests

def test_schema_metadata(repo_path, options):
    """
       Validate the metadata of a schema.json file.

       - it has a $schema, and the schema points to https://json-schema.org/draft/2020-12/schema
       - it has a modelTags (even if it is empty) just a warning
       - it has a $schemaVersion, and it is of the format XX.XX.XX
       - it has a title and the title is long enough
       - it has a description and it is long enough
       - it has a $id and the $id points to a real site
       - it has a derivedFrom (even if it is empty) just a warning
       - it has a required section and contains 'id' and 'type'
       - it has a license (even if it is empty) just a warning

       Parameters:
           file_path (str): The path to the schema.json file.

       Returns:
           tuple: (success: bool, message: str)
       """
    # minimum accepted description length in characters
    minDescriptionLength = 50
    # minimum accepted title length in characters
    minTitleLength = 15

    test_name = "Validating schema.json metadata"
    success = True
    output = []

    # Example usage of the options parameter (optional, for future flexibility)
    unpublished = not options.get("published", False)
    private = options.get("private", True)

    try:
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        # Check for $schema and validate its value
        if "$schema" not in schema:
            success = False
            output.append("*** $schema is missing")
        else:
            if schema["$schema"] != "https://json-schema.org/draft/2020-12/schema":
                success = False
                output.append(f"*** $schema is not pointing to https://json-schema.org/draft/2020-12/schema (found: {schema['$schema']})")
            else:
                output.append("$schema is valid")

        # Check for modelTags and warn if empty
        if "modelTags" not in schema:
            success = False
            output.append("*** modelTags is missing")
        else:
            if not schema["modelTags"]:
                output.append("Warning: modelTags is empty")
            else:
                output.append("modelTags is present and not empty")

        # Check for $schemaVersion and validate its format (up to 2 digits per segment)
        if "$schemaVersion" not in schema:
            success = False
            output.append("*** $schemaVersion is missing")
        else:
            version_pattern = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{1,2}$")
            if not version_pattern.match(schema["$schemaVersion"]):
                success = False
                output.append(f"*** $schemaVersion is not in the correct format (XX.XX.XX) (found: {schema['$schemaVersion']})")
            else:
                output.append("$schemaVersion is valid")

        # Check for title and ensure it is at least minTitleLength characters long
        if "title" not in schema:
            success = False
            output.append("*** title is missing")
        else:
            if len(schema["title"]) < minTitleLength:
                success = False
                output.append(f"*** title is too short (minimum {minTitleLength} characters) (found: {len(schema['title'])} characters)")
            else:
                output.append("title is valid")

        # Check for description and ensure it is at least 50 characters long
        if "description" not in schema:
            success = False
            output.append("*** description is missing")
        else:
            if len(schema["description"]) < minDescriptionLength:
                success = False
                output.append(f"*** description is too short (minimum {minDescriptionLength} characters) (found: {len(schema['description'])} characters)")
            else:
                output.append("description is valid")

        # Check for $id and validate that it points to a real site
        if "$id" not in schema:
            success = False
            output.append("*** $id is missing")
        else:
            try:
                response = requests.get(schema["$id"])
                if response.status_code != 200:
                    if unpublished:
                        success = True
                        output.append("Warning the $id is  not pointing to a valid url. Check when publishing")
                    else:
                        # the model is published 
                        success = False
                        output.append(f"*** $id does not point to a valid site (status code: {response.status_code})")
                else:
                    output.append("$id is valid and points to a real site")
            except requests.RequestException as e:
                success = False
                output.append(f"*** $id is not reachable: {e}")

        # Check for derivedFrom (even if empty) and report a warning if empty
        if "derivedFrom" not in schema:
            success = True
            output.append("Warning: derivedFrom is missing")
        else:
            if not schema["derivedFrom"]:
                output.append("Warning: derivedFrom is empty")
            else:
                output.append("derivedFrom is present and not empty")

        # Check for required section and ensure it contains 'id' and 'type'
        if "required" not in schema:
            success = False
            output.append("*** required section is missing")
        else:
            required_fields = schema["required"]
            if not isinstance(required_fields, list):
                success = False
                output.append("*** required section is not a list")
            else:
                if "id" not in required_fields:
                    success = False
                    output.append("*** 'id' is missing in the required section")
                if "type" not in required_fields:
                    success = False
                    output.append("*** 'type' is missing in the required section")
                if "id" in required_fields and "type" in required_fields:
                    output.append("required section is valid and contains 'id' and 'type'")

        # Check for license (even if empty) and report a warning if empty
        if "license" not in schema:
            output.append("Warning: license is missing")
        else:
            if not schema["license"]:
                output.append("Warning: license is empty")
            else:
                output.append("license is present and not empty")

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output
