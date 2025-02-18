import json
import os
import jsonref  # Import jsonref to handle $ref references

def extract_attributes_from_payload(payload):
    """
    Recursively extract all attributes from a JSON payload.
    """
    attributes = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            attributes.add(key)
            attributes.update(extract_attributes_from_payload(value))
    elif isinstance(payload, list):
        for item in payload:
            attributes.update(extract_attributes_from_payload(item))
    return attributes

def extract_attributes_from_schema(schema):
    """
    Recursively extract all attributes defined in a JSON schema, including those from $ref references.
    """
    attributes = set()

    # Handle properties
    if "properties" in schema:
        for key, value in schema["properties"].items():
            attributes.add(key)
            if isinstance(value, dict):
                attributes.update(extract_attributes_from_schema(value))

    # Handle nested arrays
    if "items" in schema and isinstance(schema["items"], dict):
        attributes.update(extract_attributes_from_schema(schema["items"]))

    # Handle allOf clauses
    if "allOf" in schema:
        for item in schema["allOf"]:
            attributes.update(extract_attributes_from_schema(item))

    return attributes

def test_duplicated_attributes(repo_to_test, options):
    """
    Test that all attributes in the JSON payload are defined in the schema.
    Returns:
        test_name (str): Name of the test.
        success (bool): True if all attributes are defined, False otherwise.
        output (list): List of messages describing the results of the test.
    """
    schema_file = os.path.join(repo_to_test, "schema.json")
    payload_file = os.path.join(repo_to_test, "examples/example.json")

    if not os.path.exists(schema_file):
        return "Checking that all payload attributes are defined in the schema", False, ["Schema file not found."]
    if not os.path.exists(payload_file):
        return "Checking that all payload attributes are defined in the schema", False, ["Payload file not found."]

    # Load the schema and resolve $ref references using jsonref
    with open(schema_file, 'r') as f:
        schema = jsonref.load(f, base_uri=os.path.dirname(schema_file))

    # Load the payload
    with open(payload_file, 'r') as f:
        payload = json.load(f)

    output = []

    # Extract attributes from the payload and schema
    payload_attributes = extract_attributes_from_payload(payload)
    schema_attributes = extract_attributes_from_schema(schema)

    # Check for attributes in the payload that are not in the schema
    for attribute in payload_attributes:
        if attribute not in schema_attributes:
            output.append(f"*** Attribute '{attribute}' in the payload is not defined in the schema.")

    # Determine if the test was successful
    success = len(output) == 0

    test_name = "Checking that all payload attributes are defined in the schema"
    return test_name, success, output