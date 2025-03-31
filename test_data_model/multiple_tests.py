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

from sys import argv
from json import loads, dump
from requests import get
from datetime import datetime
from master_tests import quality_analysis

def get_subdirectories(subject_root):
    """
    Get the list of first-level subdirectories in the specified root directory of a GitHub repository.

    Parameters:
        repo_url (str): The URL of the GitHub repository.
        root_directory (str): The root directory to list subdirectories from.

    Returns:
        list: List of subdirectory names.
    """
    # Extract the owner and repo name from the URL
    # TODO: Only work with tree structure and not normal url to a data model
    parts = subject_root.strip("/").split("/")
    if len(parts) < 7:
        raise ValueError("Invalid subject_root URL. It must include owner, repo, branch, and root directory.")

    owner = parts[3]  # e.g., "smart-data-models"
    repo = parts[4]  # e.g., "incubated"
    branch = parts[6]  # e.g., "d7b7b48f03b9b221d141e074e1d311985ab04f25"
    root_directory = "/".join(parts[7:])  # e.g., "SMARTMANUFACTURING/dataModel.PredictiveMaintenance"

    # GitHub API URL to list contents of the root directory
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref={branch}"

    try:
        # Fetch the contents of the root directory
        response = get(api_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch directory contents: HTTP {response.status_code}")

        contents = response.json()
        return [item['name'] for item in contents if item['type'] == 'dir']
    except Exception as e:
        raise Exception(f"Error fetching subdirectories: {e}") from e

def run_master_tests(subject_root: str, subdirectory: str, email:str, only_report_errors: bool):
    """
    Run the master_tests.py script for a specific subdirectory.

    Parameters:
        subject_root (str): The full path to the root directory in the GitHub repository.
        subdirectory (str): The subdirectory to test.
        email (str): The email address for reporting results.
        only_report_errors (bool): Whether to report only errors.

    Returns:
        dict: The results from master_tests.py.
    """
    try:
        # Remove any trailing slashes and append the subdirectory
        subject_root = subject_root.rstrip("/")
        subdirectory_url = f"{subject_root}/{subdirectory}"
        print(f"Testing subdirectory: {subdirectory_url}")

        result = quality_analysis(raw_base_url=subdirectory_url,
                                  email=email,
                                  only_report_errors=only_report_errors)

        # Parse the output as JSON
        return loads(result)
    except Exception as e:
        print(f"Error running tests for {subdirectory}: {e}")
        return {"error": str(e)}

def main():
    if len(argv) != 4:
        print("Usage: python3 multiple_tests.py <subject_root> <email> <only_report_errors>")
        exit(1)

    subject_root = argv[1]
    email = argv[2]
    only_report_errors = argv[3].lower() == "true"

    # Get the list of subdirectories
    subdirectories = get_subdirectories(subject_root)

    # Run tests for each subdirectory and collect results
    results = []

    results = \
        [{"datamodel": subdirectory,
          "result": run_master_tests(subject_root, subdirectory, email, only_report_errors)}
         for subdirectory in subdirectories]

    # Save the results to a JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"test_results_{timestamp}.json"
    with open(output_filename, "w") as f:
        dump(results, f, indent=4)

    print(f"Test results saved to {output_filename}")

if __name__ == "__main__":
    main()