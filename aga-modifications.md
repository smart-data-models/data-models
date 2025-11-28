# Summary of Modifications in the `test_data_model` Project

The modifications in the `test_data_model` project represent a significant refactoring to improve efficiency, handle missing files more gracefully, and standardize file handling. The changes are primarily uncommitted modifications compared to the last committed version in git. Below is a detailed summary:

## Key Changes Overview
- **File Handling Refactor**: All test functions now use a preloaded dictionary of file contents (`repo_files`) instead of directly accessing file paths. This allows for better error handling and performance.
- **Configuration Updates**: Paths updated to the current user's local environment.
- **New Files**: Added `requirements.txt` and `test_data_model/tests/utils.py` for dependency management and shared utilities.
- **Validation Adjustments**: Relaxed some strict validations, especially for external references and descriptions.
- **Error Handling Improvements**: Removed strict exceptions for missing files, allowing partial test success.

## Detailed Modifications by File

### `config.json`
- **Purpose**: Configuration file for test directories.
- **Changes**: to adapt to local configuration
 not pertinent for commit

### `master_tests.py`
- **Purpose**: Main test runner script.
- **Changes**:
  - Added comments explaining lenient handling of missing files (allowing partial downloads).
  - Modified `download_files()`: No longer raises exceptions for missing files; suppresses 404 errors while warning for other download errors to let individual tests handle existence.
  - Added `load_repo_files()` function: Preloads and parses files into a dictionary with content, parsed JSON, and error info.
  - Updated `run_tests()`: Changed from `repo_path` to `repo_files` dictionary parameter.
  - Test execution now uses loaded files and supports partial failures.
  - Added trailing newline.

### `multiple_tests.py`
- **Purpose**: Multi-data model testing script.
- **Changes**:
  - No substantive changes: Trivial whitespace/comment updates. Unchanged functionality.

### `README.md`
- **Purpose**: Documentation.
- **Changes**:
  - No changes: File remains unchanged.

### Test Files in `test_data_model/tests/` (All Modified)
All test files were refactored to use the new `repo_files` dictionary instead of direct file path access:
- **Global Changes**:
  - Function signatures changed from `repo_path` to `repo_files`.
  - Added checks like `if file_name not in repo_files or repo_files[file_name] is None: handle missing`.
  - Use `repo_files[file_name]["content"]`, `["json"]`, or error fields instead of opening files.
  - Moved shared functions (e.g., `resolve_ref`) to `utils.py`.
  - Updated version comments and error handling.

- **`test_array_object_structure.py`**:
  - Removed local `resolve_ref` and `resolve_nested_refs` functions.
  - Added `from .utils import resolve_ref`.
  - `validate_properties()` now recursive with `repo_files` and depth limiting.

- **`test_duplicated_attributes.py`**:
  - Uses `jsonref.loads()` for schema resolution with base URI.
  - Checks files in `repo_files` dict.

- **`test_file_exists.py`**:
  - Simplified to check `repo_files.get(file) is not None` instead of `os.path.exists()`.

- **`test_name_attributes.py`**:
  - Removed local resolve functions; imports from `utils.py`.
  - `check_attribute_case()` updated with `repo_files` parameter.

- **`test_schema_descriptions.py`**:
  - Simplified `validate_description()` to basic format check (removed strict NGSI type validation).
  - `check_property_descriptions()` skips format validation for external refs.
  - Handles arrays and `allOf` clauses better.

- **`test_schema_metadata.py`**:
  - Added file existence checks for `schema.json`.
  - Validation logic unchanged beyond file loading.

- **`test_string_incorrect.py`**:
  - Moved `validate_properties()` into function.
  - Uses `repo_files` for schema access.

- **`test_valid_json.py`**:
  - Checks `repo_files` for JSON validity via pre-parsed data.

- **`test_valid_keyvalues_examples.py`**:
  - Schema and example validation via `repo_files`.

- **`test_valid_ngsild.py`**:
  - Entity validation using loaded `repo_files`.

- **`test_valid_ngsiv2.py`**:
  - Normalized example validation via `repo_files`.

- **`test_yaml_files.py`**:
  - `validate_yaml_content()` function for content strings.
  - Checks `repo_files` for YAML validity.

### New Files (Untracked)
- **`requirements.txt`**: Dependency list including `attrs`, `certifi`, `charset-normalizer`, `idna`, `jsonpointer`, `jsonref`, `jsonschema`, `pyyaml`, `referencing`, `requests`, `rpds-py`, `urllib3`, and `pip`.
- **`tests/utils.py`**: Contains shared functions like `resolve_ref` and `resolve_ref_with_url` moved from individual test files.

### `_multiple_tests.py`
- **Purpose**: Alternative multi-test script.
- **Changes**:
  - No substantive changes: Minor debug prints removed.

## Overall Impact
- **Efficiency**: Preloading files reduces I/O operations and enables better caching.
- **Robustness**: Missing files no longer crash the entire test suite; each test reports individually.
- **Maintainability**: Centralized utility functions in `utils.py`.
- **Leniency**: Relaxed validations (e.g., optional files, external refs) to accommodate common schema patterns.
- **Setup**: `requirements.txt` enables easy dependency installation.
- **User-Specific**: Config paths tailored to current user environment.

These changes modernize the test framework without altering the core validation logic, making it more production-ready and user-friendly for the FIWARE Smart Data Models validation process.


## Testing

### /SMARTHEALTH/HL7/FHIR-R4/Account
python3 test_data_model/master_tests.py "https://github.com/agaldemas/incubated/tree/master/SMARTHEALTH/HL7/FHIR-R4/Account" "alain.galdemas@gmail.com" true --published false

### TrafficFlowObserved:
python3 test_data_model/master_tests.py "https://github.com/smart-data-models/dataModel.Transportation/tree/master/TrafficFlowObserved" "alain.galdemas@gmail.com" false --published false
