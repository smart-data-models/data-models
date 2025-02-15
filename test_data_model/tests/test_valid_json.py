import json

def test_valid_json(file_path, options):
    """
    Test if a file contains valid JSON.

    Parameters:
        file_path (str): The path to the file to check.

    Returns:
        tuple: (success: bool, message: str)
    """
    test_name = "Checking that the mandatory json files are valid json files"
    mandatory_json_files = ["schema.json", "examples/example.json", "examples/example-normalized.json", "examples/example.jsonld", "examples/example-normalized.jsonld"]
    success = True
    output = []

    # Example usage of the options parameter (optional, for future flexibility)
#    if options.get("published", False):
#        unpublished = True
#    if options.get("private", False):
#        output.append("This is a private model.")



    for file in mandatory_json_files:

        try:
            local_path = file_path + "/" + file
            # print(f"The local path to the file is {local_path}")
            with open(local_path, 'r') as local_file:
                json.load(local_file)
            success = success and True
            output.append(f"file {file} is a valid json")

        except json.JSONDecodeError as e:
            success = success and False
            output.append(f"*** file {file} is NOT a valid json")

        except FileNotFoundError:
            success = success and False
            output.append(f"*** file {file} is NOT FOUND")

    return test_name, success, output


