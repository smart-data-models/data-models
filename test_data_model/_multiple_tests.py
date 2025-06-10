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
import subprocess
import requests
from datetime import datetime
import json


def get_subdirectories(subject_root):
    """
    Get the list of first-level subdirectories in the specified root directory of a GitHub repository.

    Parameters:
        subject_root (str): The full path to the root directory in the GitHub repository.

    Returns:
        list: List of subdirectory names.
    """
    try:
        # Validate URL format
        if not subject_root.startswith("https://github.com/"):
            raise ValueError("URL must start with 'https://github.com/'")

        if "/tree/" not in subject_root:
            raise ValueError("URL must contain '/tree/' before the branch name")

        # Extract the owner, repo, branch, and root directory from the subject_root
        parts = subject_root.strip("/").split("/")
        if len(parts) < 7:
            raise ValueError("Invalid subject_root URL. It must include owner, repo, branch, and root directory.")

        owner = parts[3]
        repo = parts[4]
        branch = parts[6]
        root_directory = "/".join(parts[7:])

        # GitHub API URL to list contents of the root directory
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref={branch}"

        # Fetch the contents of the root directory
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


def run_master_tests(subject_root, subdirectory, email, only_report_errors):
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
        print("before directory")
        print(subject_root)
        subject_root = subject_root.rstrip("/")
        print(subdirectory)
        subdirectory_url = f"{subject_root}/{subdirectory}"
        print(f"Testing subdirectory: {subdirectory_url}")

        # Run the master_tests.py script
        result = subprocess.run(
            [
                "python3", "master_tests.py",
                subdirectory_url,
                email,
                "1" if only_report_errors else "0"
            ],
            capture_output=True,
            text=True
        )

        # Parse the output as JSON
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running tests for {subdirectory}: {e}")
        return {"error": str(e)}

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 multiple_tests.py <subject_root> <email> <only_report_errors>")
        sys.exit(1)

    ### remove
    print(sys.argv[1])
    subject_root = sys.argv[1]
    email = sys.argv[2]
    only_report_errors = sys.argv[3].lower() == "true"

    # Get the list of subdirectories
    subdirectories = get_subdirectories(subject_root)
    # Run tests for each subdirectory and collect results
    results = []
    print(subdirectories)
    for subdirectory in subdirectories:
        print(f"Running tests for {subdirectory}...")
        test_result = run_master_tests(subject_root, subdirectory, email, only_report_errors)
        ### remove
        print(test_result)
        # for item in test_result:
        #     print(item)
        #     item["datamodel"] = subdirectory
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