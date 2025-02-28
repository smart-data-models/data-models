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

import sys
import json
import subprocess
import requests
from datetime import datetime

def get_subdirectories(repo_url, root_directory):
    """
    Get the list of first-level subdirectories in the specified root directory of a GitHub repository.

    Parameters:
        repo_url (str): The URL of the GitHub repository.
        root_directory (str): The root directory to list subdirectories from.

    Returns:
        list: List of subdirectory names.
    """
    # Extract the owner and repo name from the URL
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    # GitHub API URL to list contents of the root directory
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            # Filter out only directories
            subdirectories = [item['name'] for item in contents if item['type'] == 'dir']
            return subdirectories
        else:
            raise Exception(f"Failed to fetch directory contents: HTTP {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching subdirectories: {e}")

def run_master_tests(repo_url, subdirectory, email, only_report_errors):
    """
    Run the master_tests.py script for a specific subdirectory.

    Parameters:
        repo_url (str): The URL of the GitHub repository.
        subdirectory (str): The subdirectory to test.
        email (str): The email address for reporting results.
        only_report_errors (bool): Whether to report only errors.

    Returns:
        dict: The results from master_tests.py.
    """
    try:
        # Construct the full URL to the subdirectory
        subdirectory_url = f"{repo_url}/tree/master/{subdirectory}"
        print(subdirectory_url)
        # Run the master_tests.py script
        result = subprocess.run(
            [
                "python3", "master_tests.py",
                subdirectory_url,
                email,
                "true" if only_report_errors else "false"
            ],
            capture_output=True,
            text=True
        )

        # Parse the output as JSON
        return json.loads(result.stdout)
    except Exception as e:
        print("hemos tenido un error")
        return {"error": str(e)}

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 multiple_tests.py <repo_url> <root_directory> <email> <only_report_errors>")
        sys.exit(1)

    repo_url = sys.argv[1]
    root_directory = sys.argv[2]
    email = sys.argv[3]
    only_report_errors = sys.argv[4].lower() == "true"

    # Get the list of subdirectories
    subdirectories = get_subdirectories(repo_url, root_directory)
    print(subdirectories)
    # Run tests for each subdirectory and collect results
    results = []
    for subdirectory in subdirectories:
        print(f"Running tests for {subdirectory}...")
        test_result = run_master_tests(repo_url, root_directory + "/" + subdirectory, email, only_report_errors)
        for item in test_result:
            print(item)
            item["datamodel"] = subdirectory
        results.append({
            "datamodel": subdirectory,
            "result": test_result
        })

    # Save the results to a JSON file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"test_results_{timestamp}.json"
    with open(output_filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Test results saved to {output_filename}")

if __name__ == "__main__":
    main()