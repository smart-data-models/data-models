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
import requests
from datetime import datetime
import json

from master_tests import quality_analysis


def get_api_url(subject_root):
    """
    Construct the GitHub API URL to list the contents of a directory.

    Accepts either a 'https://github.com/<owner>/<repo>/tree/<branch>/<path>'
    URL, or a plain 'https://github.com/<owner>/<repo>/<path>' one (which is
    assumed to be on the 'master' branch) -- previously only the first form
    was accepted at all.

    Parameters:
        subject_root (str): The URL of the GitHub repository, including the root directory.

    Returns:
        str: The GitHub API URL.

    Raises:
        ValueError: If the subject_root URL is invalid.
    """
    if not subject_root.startswith("https://github.com/"):
        raise ValueError("URL must start with 'https://github.com/'")

    parts = subject_root.strip("/").split("/")
    if len(parts) < 5:
        raise ValueError("Invalid subject_root URL. It must include at least owner and repo.")
    owner = parts[3]
    repo = parts[4]

    if "tree" in parts:
        if len(parts) < 7:
            raise ValueError("Invalid subject_root URL. It must include owner, repo, branch, and root directory.")
        branch = parts[6]
        root_directory = "/".join(parts[7:])
        return f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref={branch}"
    else:
        root_directory = "/".join(parts[5:])
        return f"https://api.github.com/repos/{owner}/{repo}/contents/{root_directory}?ref=master"


def get_subdirectories(subject_root):
    """
    Get the list of first-level subdirectories in the specified root directory of a GitHub repository.

    Parameters:
        subject_root (str): The full path to the root directory in the GitHub repository.

    Returns:
        list: List of subdirectory names.
    """
    try:
        api_url = get_api_url(subject_root)
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            return [item['name'] for item in contents if item['type'] == 'dir']
        else:
            raise Exception(f"Failed to fetch directory contents: HTTP {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching subdirectories: {e}") from e


def run_master_tests(subject_root, subdirectory, email, only_report_errors):
    """
    Run quality_analysis() for a specific subdirectory.

    Calls quality_analysis() directly (in-process) rather than shelling out
    to `python3 master_tests.py ...` and parsing its stdout as JSON -- that
    approach spawns a fresh interpreter per model and silently breaks if
    anything in the dependency chain prints something unexpected to stdout.

    Parameters:
        subject_root (str): The full path to the root directory in the GitHub repository.
        subdirectory (str): The subdirectory to test.
        email (str): The email address for reporting results.
        only_report_errors (bool): Whether to report only errors.

    Returns:
        dict: The results from quality_analysis().
    """
    try:
        subdirectory_url = f"{subject_root.rstrip('/')}/{subdirectory}"
        print(f"Testing subdirectory: {subdirectory_url}")
        return quality_analysis(
            base_url=subdirectory_url,
            email=email,
            only_report_errors=only_report_errors
        )
    except Exception as e:
        print(f"Error running tests for {subdirectory}: {e}")
        return {"error": str(e)}

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 multiple_tests.py <subject_root> <email> <only_report_errors>")
        sys.exit(1)

    subject_root = sys.argv[1]
    email = sys.argv[2]
    only_report_errors = sys.argv[3].lower() == "true"

    # Get the list of subdirectories
    subdirectories = get_subdirectories(subject_root)
    # Run tests for each subdirectory and collect results
    results = []
    for subdirectory in subdirectories:
        print(f"Running tests for {subdirectory}...")
        test_result = run_master_tests(subject_root, subdirectory, email, only_report_errors)
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