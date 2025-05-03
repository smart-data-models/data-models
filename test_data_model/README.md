# Smart Data Models Validator

This Python script validates the structure and contents of a directory containing the basic files for an official Smart Data Model (it local folder) containing standard data models and supporting files. It checks the presence and correctness of JSON schemas, examples, and YAML documentation using a set of predefined tests according to the [contribution manual](https://bit.ly/contribution_manual).

## 🚀 Features

- Supports both **GitHub URLs** and **local paths**
- Downloads all the required files  like `schema.json`, `examples/*.json`, `ADOPTERS.yaml`, and more
- Runs a series of validation tests and outputs structured JSON results
- Configuration-driven paths for results and downloads
- Parallel file downloading for GitHub sources
- Cleanup of temporary files after execution

---

## 🧪 How to Use

### 📦 Prerequisites

- Python 3.6 or newer
- `requests` library (`pip install requests`)

### 📁 Configuration

Edit the `config.json` file with the following structure:


You need to configure the script by editing the file:

[config.json](https://github.com/smart-data-models/data-models/blob/master/test_data_model/config.json)

This the content of the file config.json
```json
{
  "results_dir": "Put a local directory where the script can write, and it will store the results for the tests",
  "results_dir_help": "Nothing to edit here it is just instructions",
  "download_dir": "Put a local directory where the files being tested can be temporary stored (they are removed by the end of the test)",
  "download_dir_help": "Nothing to edit here it is just instructions"
}
```
### Usage

The file [master_tests.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/master_tests.py) can be called:

```
python3 master_tests.py <directory_root> <email> <only_report_errors> [--published true|false] [--private true|false] [--output output.json]
```

- '<repo_url_or_local_path>'. It is the local path or url for the repository where the data model is located. It does not matter because any case the files are copied locally and removed once the tests has finished. Independently if you are going to test one file or all of them the parameter of the function has to be the root of the directory where the files are located. The expect structure is described in the [contribution manual](https://bit.ly/contribution_manual). In example https://github.com/smart-data-models/dataModel.Weather/tree/master/WeatherObserved
![file structure](data_model_files_structure.png "Data model file structure")
- '< email >' is the email of the user running the test
- '<only_report_errors>' is a boolean (true or 1) to show just only those unsuccessful tests

The file [master_tests.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/master_tests.py) executes all the files in the tests directory as long as they are included in this line of code 

```
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
```
so if you create a new test you need to extend this line with your file. Bear in mind these points
1) that the file you create has to have a function with the same name of the file inside. The file [test_schema_descriptions.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/tests/test_schema_descriptions.py) has a function named test_schema_descriptions  
2) Every function returns 3 values. 
   - test_name. test_name is the description of the test run,
   - success. success is a boolean value indicating if the overall test has been successful.
   - output. output contains all the messages for the issues or successful passed tests in a json format to be easily manageable. 

# 🔍 Smart Data Models Multi-Data Model Validator

This script automates the validation of multiple data models within a GitHub repository or a local directory by invoking the [`master_tests.py`](./master_tests.py) script on each one. 

---

## 📦 Overview

- Automatically lists **first-level subdirectories** of a specified GitHub folder
- Executes `master_tests.py` for each subdirectory
- Aggregates all validation results into a single timestamped JSON file with the results of the tests
- Supports filtering to report only errors

---

## 🧰 Requirements

- Python 3.6+
- Dependencies:
  - `requests` (for GitHub API)
- [`master_tests.py`](./master_tests.py) must be available in the same directory and executable

Install required Python packages if needed:

```bash
pip install requests
```

### Usage
```
python3 multiple_tests.py <subject_root> <email> <only_report_errors>
```

| Parameter            | Description                                                                            |
| -------------------- |----------------------------------------------------------------------------------------|
| `subject_root`       | Full GitHub URL or local directory to the directory containing subfolders to be tested |
| `email`              | Email used in naming result files and tagging output                                   |
| `only_report_errors` | `true` or `false` (case-insensitive) — limits output to failed tests only              |

#### Output

The script creates a JSON file named like test_results_YYYY-MM-DD_HH-MM-SS.json containing all subdirectory test results.

Each entry in the output JSON has:

- The subdirectory name (datamodel)
- The result as returned by master_tests.py


### Contact

For questions, bug reports, or feedback, please use the Issues tab or contact:
Your Name or Team
📧 info@smartdatamodels.org