import json 
def test_duplicated_attributes(repo_path, options):
    """
    Test if any attributes in the schema.json file are duplicated at the same object level,
    taking into account allOf and oneOf clauses.

    Parameters:
        repo_path (str): The path to the repository containing the schema.json file.
        options (dict): Additional options for the test (e.g., {"published": True, "private": False}).

    Returns:
        tuple: (test_name: str, success: bool, output: list)
    """
    test_name = "Checking for duplicated attributes in schema.json"
    success = True
    output = []

    # Example usage of the options parameter
    if options.get("published", False):
        output.append("This is an officially published model.")
    if options.get("private", False):
        output.append("This is a private model.")

    try:
        # Load the schema.json file
        with open(f"{repo_path}/schema.json", 'r') as file:
            schema = json.load(file)

        # Find duplicates in the schema
        duplicates = find_duplicates_in_object(schema)

        # Report duplicates
        if duplicates:
            success = False
            output.append("*** Duplicated attributes found:")
            for duplicate in duplicates:
                output.append(f"*** - {duplicate}")
        else:
            output.append("No duplicated attributes found.")

    except json.JSONDecodeError:
        success = False
        output.append("*** schema.json is not a valid JSON file")
    except FileNotFoundError:
        success = False
        output.append("*** schema.json file not found")

    return test_name, success, output
