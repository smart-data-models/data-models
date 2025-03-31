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

from json import dump, dumps, load
from importlib import import_module
from os.path import join, dirname, exists
from os import makedirs
from requests import get
from shutil import copy, rmtree
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from argparse import ArgumentParser # Import argparse for command-line argument parsing
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Loads configuration data from a JSON file, searching default locations if a path isn't provided.
    It also validates that required keys are present and converts specific paths to absolute paths.

    Parameters:
        config_path (str, optional): The path to the configuration file. If None, default locations are searched.

    Returns:
        Dict[str, Any]: The loaded configuration data.

    Raises:
        FileNotFoundError: If no configuration file is found.
        ValueError: If required keys are missing in the configuration.
    """
    default_locations = [
        Path("config.json"),
        Path.home() / ".your_package_config.json",
        Path(__file__).parent / "config.json"
    ]

    if config_path is None:
        for location in default_locations:
            if location.exists():
                config_path = location
                break
        else:
            raise FileNotFoundError("No configuration file found in default locations")

    with open(config_path, 'r') as f:
        config = load(f)

    required_keys = ['results_dir', 'download_dir']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    config['results_dir'] = str(Path(config['results_dir']).expanduser().absolute())
    config['download_dir'] = str(Path(config['download_dir']).expanduser().absolute())

    return config


def is_url(path):
    """
    Check if the provided path is a URL.

    Parameters:
        path (str): The path to check.

    Returns:
        bool: True if the path is a URL, False otherwise.
    """
    return path.startswith(("http://", "https://"))


def convert_github_url_to_raw(subject_root):
    """
    Convert a GitHub repository URL to the corresponding raw file URL.

    Parameters:
        subject_root (str): The GitHub repository URL (e.g., https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/schema.json).

    Returns:
        str: The raw file base URL (e.g., https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/refs/heads/master/WeatherObserved/).
    """
    try:
        if "github.com" not in subject_root:
            raise ValueError("Invalid GitHub repository URL.")

        # Handle master branch URLs
        if "/blob/" in subject_root:
            return _extracted_from_convert_github_url_to_raw(
                subject_root, "/blob/", "/"
            )
        elif "/tree/" in subject_root:
            return _extracted_from_convert_github_url_to_raw(subject_root, "/tree/", "/")
        else:
            parts = subject_root.split('/')
            url = '/'.join(parts[:-1]) + '/refs/heads/master/' + parts[-1]
            return f"{url.replace("github.com", "raw.githubusercontent.com")}"
    except Exception as e:
        raise ValueError(f"Error converting GitHub URL to raw URL: {e}") from e


def _extracted_from_convert_github_url_to_raw(repo_url: str, arg1: str, arg2: str) -> str:
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
    return raw_url.replace(arg1, arg2)


def download_file(url: str, file_path):
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
        makedirs(name=dirname(p=file_path), exist_ok=True)

        # Download the file
        response = get(url=url, timeout=10)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path, True, "Download successful"
    except Exception as e:
        return file_path, False, f"Error downloading {url}: {e}"


def download_files(subject_root: str, download_dir: str):
    """
    Download or copy files from a URL or local directory.

    Downloads or copies a predefined set of files from a given URL or local directory to a specified download directory.
    If the source is a URL, parallel downloads are used. If it's a local path, files are copied.

    Parameters:
        subject_root (str): The URL or local path to download/copy files from.
        download_dir (str): The directory to save the downloaded/copied files.

    Returns:
        str: The path to the download directory.

    Raises:
        Exception: If any error occurs during download or copying.
    """
    try:
        # Ensure the download directory exists
        makedirs(download_dir, exist_ok=True)

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

        if is_url(subject_root):
            # Download files from a URL using parallel threads
            with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
                futures = []
                for file in files_to_download:
                    file_url = f"{subject_root.rstrip('/')}/{file}"
                    file_path = join(download_dir, file)
                    futures.append(executor.submit(download_file, file_url, file_path))

                # Wait for all downloads to complete and check for errors
                for future in as_completed(futures):
                    file_path, success, message = future.result()
                    if not success and message:
                        raise Exception(message)
        else:
            # Copy files from a local directory (no parallelization needed)
            for file in files_to_download:
                src_path = join(subject_root, file)
                dest_path = join(download_dir, file)

                # Ensure the directory structure exists
                makedirs(name=dirname(p=dest_path), exist_ok=True)

                # Copy the file
                if exists(src_path):
                    copy(src_path, dest_path)
                else:
                    raise Exception(f"File not found: {src_path}")

        return download_dir
    except Exception as e:
        raise Exception(f"Error downloading/copying files: {e}")


def run_tests(test_files: list, repo_to_test: str, only_report_errors: bool, options: dict) -> dict:
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
            module = import_module(f"tests.{test_file}")
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
    try:
        parser = ArgumentParser(description="Run tests on a repository.")
        # https://github.com/smart-data-models/dataModel.DCAT-AP/tree/a0b2ee1a86be25fa896103c10c0a943558a7d6d2/Agent alberto.abella@fiware.org 0
        # Mandatory arguments
        parser.add_argument("subject_root", type=str, help="The subject root of the repository to check.")
        parser.add_argument("email", type=str, help="The email address for reporting results.")
        parser.add_argument("only_report_errors", type=str, help="Whether to report only errors (true/false or 1/0).")

        # Optional arguments
        parser.add_argument("--published", type=str, help="Whether the model is officially published (true/false or 1/0).", default="false")
        parser.add_argument("--private", type=str, help="Whether the model is private (true/false or 1/0).", default="false")
        parser.add_argument("--output", type=str, help="Additional output file path for the test results.", default=None)

        # Parse arguments
        args = parser.parse_args()

        # Convert string arguments to appropriate types
        only_report_errors = args.only_report_errors.lower() in ("true", "1")
        published = args.published.lower() in ("true", "1")
        private = args.private.lower() in ("true", "1")
        output_file = args.output

        # Validate the email (basic check)
        if not args.email or "@" not in args.email:
            raise ValueError("Missing or invalid email address")

        return quality_analysis(base_url=args.subject_root,
                                published=published,
                                private=private,
                                only_report_errors=only_report_errors,
                                email=args.email,
                                output_file=output_file)
    except Exception as e:
        Exception(f"Error analyzing the data model: {e}")


def quality_analysis(base_url: str, email: str, only_report_errors: bool, published: bool =False,
                     private: bool =False, output_file: str =None) -> dict | None:
    result = {
        "success": False,
        "error": None,
        "test_results": None,
        "metadata": {
            "timestamp": datetime.now().isoformat()
        }
    }

    # Validate the subject_root, if the input is a URL, convert it to a raw file base URL
    if is_url(base_url):
        raw_base_url = convert_github_url_to_raw(base_url)
    else:
        raw_base_url = base_url

    config = load_config()
    results_dir = config['results_dir']
    download_dir = config['download_dir']

    Path(results_dir).mkdir(parents=True, exist_ok=True)
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    try:
        # Download or copy the files
        repo_path = download_files(raw_base_url, download_dir)

        # List of test files to run
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

        # Run the tests with the options object
        test_results = run_tests(test_files=test_files,
                                 repo_to_test=repo_path,
                                 only_report_errors=only_report_errors,
                                 options=options)

        # Add email to the results
        test_results["email"] = email

        # Display the results
        result |= {"success": True, "test_results": test_results}

        # Save a file with the results
        email_name = email.replace("@", "_at_")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{results_dir}/test_results_{timestamp}_{email_name}.json"
        with open(filename, "w") as f:
            dump(test_results, f, indent=4)

        # Save an additional copy of the results if --output is provided
        if output_file:
            with open(output_file, "w") as f:
                dump(test_results, f, indent=4)

    except Exception as e:
        result["error"] = str(e)
    finally:
        # Clean up the temporary directory
        if 'download_dir' in locals() and exists(download_dir):
            rmtree(download_dir)

        # Ensure we always print valid JSON
        print(dumps(result, indent=2))

    return result


if __name__ == "__main__":
    main()
