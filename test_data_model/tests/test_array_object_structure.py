import json
import os

def resolve_ref(repo_path, ref):
    """
    Resolve a $ref reference in the schema.

    Parameters:
        repo_path (str): The path to the schema.json file.
        ref (str): The reference to resolve (e.g., "#/definitions/SomeDefinition").

    Returns:
        dict: The resolved schema fragment.
    """
    try:
        # Split the reference into file path and JSON pointer
        if ref.startswith("#"):
            # Local reference within the same file
            with open(f"{repo_path}/schema.json", 'r') as file:
                schema = json.load(file)
            pointer = ref[1:].split("/")
            resolved = schema
            for part in pointer:
                if part in resolved:
                    resolved = resolved[part]
                else:
                    raise ValueError(f"Reference not found: {ref}")
            return resolved
        else:
            # External reference (not fully implemented here)
            raise ValueError(f"External references are not supported: {ref}")
    except Exception as e:
        raise ValueError(f"Error resolving reference {ref}: {e}")

def validate_properties(repo_path, properties, path="", success=True, output=[]):
    """
    Recursively validate properties in the schema.

    Parameters:
        repo_path (str): The path to the schema.json file.
        properties (dict): The properties to validate.
        path (str): The current path in the schema (for error messages).
        success (bool): The current success status.
        output (list): The list of error messages.

    Returns:
        tuple: (success: bool, output: list)
    """
    for key, value in properties.items():
        if isinstance(value, dict):
            # Handle $ref references
            if "$ref" in value:
                try:
                    resolved = resolve_ref(repo_path, value["$ref"])
                    success, output = validate_properties(repo_path, resolved, path + key + ".", success, output)
                except ValueError as e:
                    success = False
                    output.append(f"*** Error: Failed to resolve $ref in attribute '{path + key}': {e}")
                continue

            # Check type-specific clauses
            type_value = value.get("type", "")
            if type_value == "array" and "items" not in value:
                success = False
                output.append(f"*** Error: Attribute '{path + key}' is of type 'array' but is missing the 'items' clause.")
            elif type_value == "object" and "properties" not in value:
                success = False
                output.append(f"*** Error: Attribute '{path + key}' is of type 'object' but is missing the 'properties' clause.")

            # Recursively check nested properties
            if "properties" in value and isinstance(value["properties"], dict):
                success, output = validate_properties(repo_path, value["properties"], path + key + ".", success, output)
            if "items" in value and isinstance(value["items"], dict):
                success, output = validate_properties(repo_path, value["items"], path + key + ".", success, output)

    return success, output

def test_array_object_structure(repo_path, options):
    """
    Validate that attributes with type 'array' have an 'items' clause and
    attributes with type 'object' have a 'properties' clause, handling allOf and $ref.

    Parameters:
        repo_path (str): The path to the schema.json file.
        options (dict): Additional options for the test (unused in this test).

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking array and object attributes structure"
    success = True
    output = []

    try:
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        # Handle allOf clause
        if "allOf" in schema and isinstance(schema["allOf"], list):
            for item in schema["allOf"]:
                if isinstance(item, dict) and "properties" in item:
                    success, output = validate_properties(repo_path, item["properties"], "", success, output)
        elif "properties" in schema and isinstance(schema["properties"], dict):
            success, output = validate_properties(repo_path, schema["properties"], "", success, output)

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output