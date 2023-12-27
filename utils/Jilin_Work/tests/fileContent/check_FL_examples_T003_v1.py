# FL stands for inside file check for one data model
# this python file is focused on files under the examples folder

from utils.utils import *
import fileContent

# TODO: include geojson example in the future
CHECK_EXAMPLES = [
    'example.json',
    'example.jsonld', 
    'example-normalized.json',
    'example-normalized.jsonld'
    ]

def check_FL_examples(datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath):
    """
    Check files examples given the data model link
    """

    send_message(testnumber, mail, tz, type="loading")

    output = {"result": False}  # the json answering the test

    rawSchemaUrl = get_schema_json_raw(datamodelRepoUrl)
    metaSchema = open_jsonref(rawSchemaUrl)

    # go through all the files
    for checking_file in CHECK_EXAMPLES:

        rawExampleUrl = create_example_url_raw(datamodelRepoUrl, checking_file)
        
        send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname=f"{checking_file} check")
        
        # from normalized to keyvalue
        # validate the examples and schema.json
        cfoutput = {"result": False}

        # check the parameters
        # 1. whether example file is readable
        # 2. whether example payload is valid with schema, additional properties is not allowed
        # 3. whether properties are duplicated defined
        result = check_parameters(cfoutput, tz, jsonOutput_filepath, schemaUrl=rawExampleUrl, mail=mail, test=testnumber, metaSchema=metaSchema, tag=checking_file)
        
        # if result is false, then there exits mentioned errors
        if not result:
            return result

        # if result is true, return
        # cfoutput: the json output dictionary
        # exampleDict: the example dictionary
        cfoutput, exampleDict, _ = result
        cfoutput["result"] = True

        # check the metadata of examples
        if checking_file.endswith("ld"):
            # check id, type, @context
            cfoutput = fileContent.is_metadata_existed_examples(cfoutput, exampleDict, datamodelRepoUrl, message="example")
        else:
            # check id, type
            cfoutput = fileContent.is_metadata_existed_examples(cfoutput, exampleDict, datamodelRepoUrl, message="example", checklist=['id', 'type'])
        
        output[checking_file] = cfoutput

        if cfoutput["metadata"]:
            # if metadata is not empty, then the test is failed, return the failed message
            output["cause"] = message_after_check_example(cfoutput)
            customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=False)
            return False

    try:
        # generate examples referral for example-normalized.json and example-normalized.jsonld
        generate_examples(create_example_url_raw(datamodelRepoUrl, 'example-normalized.json'),
                        create_example_url_raw(datamodelRepoUrl, 'example-normalized.jsonld'),
                        output, tz, testnumber, jsonOutput_filepath, mail)
    except:
        print("Error when generating examples")

    customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail)

    return True
