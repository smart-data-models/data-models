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
from json import dump
from requests import get
from datetime import datetime
from master_tests import quality_analysis


def get_subdirectories(subject_root):
    """
    Get the list of first-level subdirectories in the specified root directory of a GitHub repository.

    Parameters:
        subject_root (str): The full path to the root directory in the GitHub repository (e.g., https://github.com/smart-data-models/incubated/tree/d7b7b48f03b9b221d141e074e1d311985ab04f25/SMARTMANUFACTURING/dataModel.PredictiveMaintenance).

    Returns:
        list: List of subdirectory names.
    """
    # Extract the owner and repo name from the URL
    api_url = get_api_url(subject_root=subject_root)

    try:
        # Fetch the contents of the root directory
        response = get(api_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch directory contents: HTTP {response.status_code}")

        contents = response.json()
        return [item['name'] for item in contents if item['type'] == 'dir']
    except Exception as e:
        raise Exception(f"Error fetching subdirectories: {e}") from e

        
def get_api_url(subject_root: str) -> str:
    """
    Construct the GitHub API URL to fetch the contents of a directory.

    Constructs the URL based on the provided subject_root, which can point to either the master branch or a specific branch/commit.
    The URL is used to retrieve directory contents from the GitHub API.

    Parameters:
        subject_root (str): The URL of the GitHub repository, including the root directory.

    Returns:
        str: The GitHub API URL.

    Raises:
        ValueError: If the subject_root URL is invalid.
    """
    # Extract the owner and repo name from the URL
    parts = subject_root.strip("/").split("/")

    owner = parts[3]  # e.g., "smart-data-models"
    repo = parts[4]  # e.g., "incubated"

    if 'tree' in parts:
        if len(parts) < 7:
            raise ValueError("Invalid subject_root URL. It must include owner, repo, branch, and root directory.")

        branch = parts[6]  # e.g., "d7b7b48f03b9b221d141e074e1d311985ab04f25"
        root_directory = "/".join(parts[7:])  # e.g., "SMARTMANUFACTURING/dataModel.PredictiveMaintenance"

        # GitHub API URL to list contents of the root directory
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref={branch}"
    else:
        if len(parts) < 5:
            raise ValueError("Invalid subject_root URL. It must include owner, repo, branch, and root directory.")

        root_directory = "/".join(parts[5:])  # e.g., "SMARTMANUFACTURING/dataModel.PredictiveMaintenance"

        # GitHub API URL to list contents of the root directory
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref=master"

    return api_url


def run_master_tests(subject_root: str, subdirectory: str, email:str, only_report_errors: bool) -> dict:
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
        # Construct the full URL to the subdirectory
        # Remove any trailing slashes and append the subdirectory
        subject_root = subject_root.rstrip("/")
        subdirectory_url = f"{subject_root}/{subdirectory}"
        print(f"Testing subdirectory: {subdirectory_url}")

        # Run the master_tests.py script
        result = quality_analysis(base_url=subdirectory_url,
                                  email=email,
                                  only_report_errors=only_report_errors)

        return result
    except Exception as e:
        print(f"Error running tests for {subdirectory}: {e}")
        return {"error": str(e)}


def main():
    """
    Main function to execute tests on multiple subdirectories of a GitHub repository.

    Retrieves the subdirectories from the specified GitHub repository URL and runs quality analysis for each subdirectory.
    The results are then saved to a JSON file.
    """
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