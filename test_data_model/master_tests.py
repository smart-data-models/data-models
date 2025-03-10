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
import importlib
import sys
import os
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse  # Import argparse for command-line argument parsing

def is_url(path):
    """
    Check if the provided path is a URL.

    Parameters:
        path (str): The path to check.

    Returns:
        bool: True if the path is a URL, False otherwise.
    """
    return path.startswith("http://") or path.startswith("https://")

def convert_github_url_to_raw(repo_url):
    """
    Convert a GitHub repository URL to the corresponding raw file URL.

    Parameters:
        repo_url (str): The GitHub repository URL (e.g., https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/schema.json).

    Returns:
        str: The raw file base URL (e.g., https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/refs/heads/master/WeatherObserved/).
    """
    try:
        if "github.com" not in repo_url:
            raise ValueError("Invalid GitHub repository URL.")

        # Handle master branch URLs
        if "/blob/master/" in repo_url:
            # Replace "github.com" with "raw.githubusercontent.com"
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            # Replace "/blob/master/" with "/refs/heads/master/"
            raw_url = raw_url.replace("/blob/master/", "/refs/heads/master/")
            return raw_url

        # Handle PR branch URLs
        elif "/tree/" in repo_url:
            # Replace "github.com" with "raw.githubusercontent.com"
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            # Replace "/tree/" with "/"
            raw_url = raw_url.replace("/tree/", "/")
            return raw_url

        else:
            raise ValueError("Unsupported GitHub URL format.")
    except Exception as e:
        raise ValueError(f"Error converting GitHub URL to raw URL: {e}")

def download_file(url, file_path):
    """
    Download a single file from a URL and save it to the specified path.

    Parameters:
        url (str): The URL of the file to download.
        file_path (str): The path where the file should be saved.

    Returns:
        tuple: (file_path, success, message)
    """
    try:
        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            return (file_path, True, "Download successful")
        else:
            return (file_path, False, f"Failed to download {url}: HTTP {response.status_code}")
    except Exception as e:
        return (file_path, False, f"Error downloading {url}: {e}")

def download_files(base_url_or_path, download_dir):
    """
    Download files from a raw GitHub base URL or copy files from a local directory using parallel threads.

    Parameters:
        base_url_or_path (str): The base URL for raw files or the local directory path.
        download_dir (str): The directory to download/copy the files into.

    Returns:
        str: The path to the downloaded/copied files.
    """
    try:
        # Ensure the download directory exists
        os.makedirs(download_dir, exist_ok=True)

        # List of files to download/copy (adjust as needed)
        files_to_download = [
            "schema.json",
            "examples/example.json",
            "examples/example-normalized.json",
            "examples/example.jsonld",
            "examples/example-normalized.jsonld",
            "ADOPTERS.yaml",
            "notes.yaml",
        ]

        if is_url(base_url_or_path):
            # Download files from a URL using parallel threads
            with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
                futures = []
                for file in files_to_download:
                    file_url = f"{base_url_or_path.rstrip('/')}/{file}"
                    file_path = os.path.join(download_dir, file)
                    futures.append(executor.submit(download_file, file_url, file_path))

                # Wait for all downloads to complete and check for errors
                for future in as_completed(futures):
                    file_path, success, message = future.result()
                    if not success:
                        raise Exception(message)
        else:
            # Copy files from a local directory (no parallelization needed)
            for file in files_to_download:
                src_path = os.path.join(base_url_or_path, file)
                dest_path = os.path.join(download_dir, file)

                # Ensure the directory structure exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Copy the file
                if os.path.exists(src_path):
                    shutil.copy(src_path, dest_path)
                else:
                    raise Exception(f"File not found: {src_path}")

        return download_dir
    except Exception as e:
        raise Exception(f"Error downloading/copying files: {e}")

def run_tests(test_files, repo_to_test, only_report_errors, options):
    """
    Run a series of tests on a file.

    Parameters:
        test_files (list): List of test module names (e.g., ["test_valid_json", "test_file_exists"]).
        repo_to_test (str): The path to the directory where the files are located.
        only_report_errors (bool): Whether to include only failed tests in the results.
        options (dict): Additional options for the tests (e.g., {"published": True, "private": False}).

    Returns:
        dict: Results of the tests.
    """
    results = {}
    for test_file in test_files:
        try:
            # Import the test module
            module = importlib.import_module(f"tests.{test_file}")
            # Run the test function (assumes the function name is the same as the module name without 'test_')
            test_function = getattr(module, test_file)
            test_name, success, message = test_function(repo_to_test, options)
            # Include the test result only if it failed or if only_report_errors is False
            if not only_report_errors or not success:
                results[test_file] = {
                    "test_name": test_name,
                    "success": success,
                    "message": message
                }
        except Exception as e:
            results[test_file] = {
                "test_name": test_file,
                "success": False,
                "message": f"Error running test: {e}"
            }
    return results

def main():
    # Set up argument parser
    # results_dir = "/var/www/html/extra/test2/results"
    results_dir = "/home/aabella/PycharmProjects/data-models/test_data_model/results"
    parser = argparse.ArgumentParser(description="Run tests on a repository.")
    
    # Mandatory arguments
    parser.add_argument("repo_url_or_local_path", type=str, help="The repository URL or local path.")
    parser.add_argument("email", type=str, help="The email address for reporting results.")
    parser.add_argument("only_report_errors", type=str, help="Whether to report only errors (true/false or 1/0).")
    
    # Optional arguments
    parser.add_argument("--published", type=str, help="Whether the model is officially published (true/false or 1/0).", default="false")
    parser.add_argument("--private", type=str, help="Whether the model is private (true/false or 1/0).", default="false")
    parser.add_argument("--output", type=str, help="Additional output file path for the test results.", default=None)
    
    # Parse arguments
    args = parser.parse_args()

    # Convert string arguments to appropriate types
    only_report_errors = args.only_report_errors.lower() == "true" or args.only_report_errors == "1"
    published = args.published.lower() == "true" or args.published == "1"
    private = args.private.lower() == "true" or args.private == "1"
    output_file = args.output

    # Validate the email (basic check)
    if not args.email or "@" not in args.email:
        print("Error: Missing or invalid email address.")
        sys.exit(1)

    # Temporary directory to download/copy the files
    # download_dir = "/var/html/www/extra/test2/repo_to_test"
    download_dir = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/GITHUB/repo_to_test"
    try:
        # If the input is a URL, convert it to a raw file base URL
        if is_url(args.repo_url_or_local_path):
            raw_base_url = convert_github_url_to_raw(args.repo_url_or_local_path)
        else:
            raw_base_url = args.repo_url_or_local_path

        # Download or copy the files
        repo_path = download_files(raw_base_url, download_dir)

        # List of test files to run
#        test_files = [
#            "test_valid_json", "test_file_exists", "test_schema_descriptions", 
#            "test_schema_metadata", "test_duplicated_attributes", "test_yaml_files", 
#            "test_valid_keyvalues_examples", "test_valid_ngsiv2", "test_valid_ngsild"
#        ]
        test_files = ["test_file_exists",
                      "test_valid_json",
                      "test_yaml_files",
                      "test_schema_descriptions",
                      "test_schema_metadata",
                      "test_string_incorrect",
                      "test_valid_keyvalues_examples",
                      "test_valid_ngsiv2",
                      "test_valid_ngsild",
                      "test_duplicated_attributes",
                      "test_array_object_structure"
                      ]

        # Create options dictionary
        options = {
            "published": published,
            "private": private
        }
        # print(options)

        # Run the tests with the options object
        test_results = run_tests(test_files, repo_path, only_report_errors, options)

        # Add email to the results
        test_results["email"] = args.email

        # Display the results
        print(json.dumps(test_results, indent=4))

        # Save a file with the results
        email_name = args.email.replace("@", "_at_")
        time_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{results_dir}/{time_name}_{email_name}.json"
        with open(filename, "w") as f:
            json.dump(test_results, f, indent=4)

        # Save an additional copy of the results if --output is provided
        if output_file:
            with open(output_file, "w") as f:
                json.dump(test_results, f, indent=4)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up the temporary directory
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)

if __name__ == "__main__":
    main()
