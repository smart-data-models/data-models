"""
Automated Smart Data Models data model directoryValidator

This script validates a given repository (a directory of the repository) or local directory by running a series of
predefined tests on expected data files (e.g., JSON, YAML) to check if the data model meet the requirements of the [contribution manual](https://bit.ly/contribution_manual)
 It supports GitHub URLs and local directories.

Usage:
    python script.py <subject_root> <email> <only_report_errors> [--published true|false] [--private true|false] [--output <output_file>]

Positional arguments:
    subject_root          URL or local path to the repository root (e.g., GitHub repo or local folder)
    email                 Contact email used for identifying results
    only_report_errors    Set to "true" to include only failed test results in the output (case-insensitive)

Optional arguments:
    --published           Mark the repository as published (default: false)
    --private             Mark the repository as private (default: false)
    --output              Path to a file where output JSON will be saved (in addition to the results' directory)

Configuration:
    The script looks for a config file (`config.json`) in one of the following locations:
      - Current directory
      - $HOME/.your_package_config.json
      - Same directory as this script

    The config file must be a valid JSON with the following keys:
      {
        "results_dir": "path/to/save/results",
        "download_dir": "path/to/temp/download"
      }

Example:
    python script.py https://github.com/example/repo user@example.com true --published true --output result.json

Note:
    - Requires Python 3.6+
    - Automatically cleans up temporary downloaded files
    - Output is always printed as JSON to stdout

Author: Alberto Abella (alberto.abella@fiware.org)
"""

import json
import importlib
import sys
import os
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import argparse
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
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
        config = json.load(f)

    required_keys = ['results_dir', 'download_dir']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    config['results_dir'] = str(Path(config['results_dir']).expanduser().absolute())
    config['download_dir'] = str(Path(config['download_dir']).expanduser().absolute())

    return config


def is_url(path):
    return path.startswith(("http://", "https://"))


def convert_github_url_to_raw(subject_root):
    try:
        if "github.com" not in subject_root:
            raise ValueError("Invalid GitHub repository URL.")

        if "/blob/" in subject_root:
            raw_url = subject_root.replace("github.com", "raw.githubusercontent.com")
            return raw_url.replace("/blob/", "/")
        elif "/tree/" in subject_root:
            raw_url = subject_root.replace("github.com", "raw.githubusercontent.com")
            return raw_url.replace("/tree/", "/")
        else:
            return subject_root.replace("github.com", "raw.githubusercontent.com") + "/master"
    except Exception as e:
        raise ValueError(f"Error converting GitHub URL to raw URL: {e}")


def download_file(url, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path, True, None
    except Exception as e:
        return file_path, False, str(e)


def download_files(subject_root, download_dir):
    try:
        os.makedirs(download_dir, exist_ok=True)
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
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for file in files_to_download:
                    file_url = f"{subject_root.rstrip('/')}/{file}"
                    file_path = os.path.join(download_dir, file)
                    futures.append(executor.submit(download_file, file_url, file_path))

                for future in as_completed(futures):
                    file_path, success, message = future.result()
                    if not success and message:
                        raise Exception(message)
        else:
            for file in files_to_download:
                src_path = os.path.join(subject_root, file)
                dest_path = os.path.join(download_dir, file)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if os.path.exists(src_path):
                    shutil.copy(src_path, dest_path)
                else:
                    raise Exception(f"File not found: {src_path}")

        return download_dir
    except Exception as e:
        raise Exception(f"Error downloading/copying files: {e}")


def run_tests(test_files, repo_to_test, only_report_errors, options):
    results = {}
    for test_file in test_files:
        try:
            module = importlib.import_module(f"tests.{test_file}")
            test_function = getattr(module, test_file)
            test_name, success, message = test_function(repo_to_test, options)
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
    result = {
        "success": False,
        "error": None,
        "test_results": None,
        "metadata": {
            "timestamp": datetime.now().isoformat()
        }
    }

    try:
        config = load_config()
        results_dir = config['results_dir']
        download_dir = config['download_dir']

        Path(results_dir).mkdir(parents=True, exist_ok=True)
        Path(download_dir).mkdir(parents=True, exist_ok=True)

        parser = argparse.ArgumentParser()
        parser.add_argument("subject_root", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("only_report_errors", type=str)
        parser.add_argument("--published", type=str, default="false")
        parser.add_argument("--private", type=str, default="false")
        parser.add_argument("--output", type=str, default=None)

        args = parser.parse_args()

        if not args.email or "@" not in args.email:
            raise ValueError("Missing or invalid email address")

        only_report_errors = args.only_report_errors.lower() in ("true", "1")
        published = args.published.lower() in ("true", "1")
        private = args.private.lower() in ("true", "1")

        if is_url(args.subject_root):
            raw_base_url = convert_github_url_to_raw(args.subject_root)
        else:
            raw_base_url = args.subject_root

        repo_path = download_files(raw_base_url, download_dir)

        test_files = [
            "test_file_exists",
            "test_valid_json",
            "test_yaml_files",
            "test_schema_descriptions",
            "test_schema_metadata",
            "test_string_incorrect",
            "test_valid_keyvalues_examples",
            "test_valid_ngsiv2",
            "test_valid_ngsild",
            "test_duplicated_attributes",
            "test_array_object_structure",
            "test_name_attributes"
        ]

        test_results = run_tests(test_files, repo_path, only_report_errors, {
            "published": published,
            "private": private
        })

        test_results["email"] = args.email
        result.update({
            "success": True,
            "test_results": test_results
        })

        email_name = args.email.replace("@", "_at_")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{results_dir}/{timestamp}_{email_name}.json"
        with open(filename, "w") as f:
            json.dump(test_results, f, indent=4)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(test_results, f, indent=4)

    except Exception as e:
        result["error"] = str(e)
    finally:
        if 'download_dir' in locals() and os.path.exists(download_dir):
            shutil.rmtree(download_dir)

        # Ensure we always print valid JSON
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()