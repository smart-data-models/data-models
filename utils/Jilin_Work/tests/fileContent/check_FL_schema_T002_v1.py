# FL stands for inside file check for one data model
# this python file is focused on schema.json file

from utils.utils import *
import fileContent

def check_FL_schemajson(datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath):
    """
    Check file schema.json given the data model link
    """

    send_message(testnumber, mail, tz, type="loading")

    output = {"result": False}  # the json answering the test

    rawSchemaUrl = get_schema_json_raw(datamodelRepoUrl)
    
    configFileName = "/home/fiware/production/tests/config_test.json"
    masterTestConfig = open_jsonref(configFileName)
    metaSchema = masterTestConfig["metaSchema"]
    metaSchema = open_jsonref(metaSchema)

    # check the parameters
    # 1. whether schema.json file is readable
    # 2. whether $ref in schema.json is extendable
    # 3. whether schema is valid
    # 4. whether properties are duplicated defined
    # 5. whether email is valid
    result = check_parameters(output, tz, jsonOutput_filepath, schemaUrl=rawSchemaUrl, mail=mail, test=testnumber, metaSchema=metaSchema, tag="schema")
    
    # if result is false, then there exits mentioned errors
    if not result:
        return result
    
    # if result is true, return
    # output: the json output dictionary
    # schemaDict: the schema json dictionary
    # yamlDict: the processed schema json dictionary
    output, schemaDict, yamlDict = result
    
    # subtest 1 - check whether the properties are well documented
    send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname="Whether properties are well documented")
    output = fileContent.is_well_documented(output, yamlDict, datamodelRepoUrl)
    
    # subtest 2 - check whether the properties are defined in the database
    send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname="Whether properties are existed in the database")
    output = fileContent.is_property_already_existed(output, yamlDict)
    
    # subtest 3 - check whether the metadata is properly reported
    send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname="Metadata part 1 (derivedFrom, license)")
    output = fileContent.is_metadata_properly_reported(output, schemaDict)
    
    # subtest 4 - check whether the metadata is existent
    send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname="Metadata part 2 ($schema, $id, title, description, modelTags, $schemaVersion, required)")
    output = fileContent.is_metadata_existed(output, schemaDict, datamodelRepoUrl, message="schema")

    # make a summary of output
    results = schema_output_sum(output)
    output["sumup_results"] = results
    
    if not results["Failed"]:
        customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail)
        return True
    else:
        # if any of the subtests is failed
        customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=False)
        return False

def schema_output_sum(output):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """

    documentationStatusOfProperties = output['documentationStatusOfProperties']
    alreadyUsedProperties = output['alreadyUsedProperties']
    availableProperties = output['availableProperties']
    metadata = output['metadata']

    results = {}
    results = {key: [] for key in CHECKED_PROPERTY_CASES}
    results['Failed'] = {}

    for pp, value in documentationStatusOfProperties.items():
        if value['documented'] & value['x-ngsi']:
            results['well documented'].append(pp)
        elif value['x-ngsi'] is False:
            if value['x-ngsi_text'] not in results['Failed'].keys():
                results['Failed'][value['x-ngsi_text']] = []
            results['Failed'][value['x-ngsi_text']].append(pp)
        elif value['documented'] is False:
            if value['text'] not in results['Failed'].keys():
                results['Failed'][value['text']] = []
            results['Failed'][value['text']].append(pp)
        if (pp == "type") and (value["type_specific"] is False):
            results['Failed'][value["type_specific_text"]] = []
            results['Failed'][value["type_specific_text"]].append(pp)
        if 'duplicated_prop' in value:
            try:
                results['Failed'][value['duplicated_prop_text']].append(pp)
            except:
                results['Failed'][value['duplicated_prop_text']] = []
                results['Failed'][value['duplicated_prop_text']].append(pp)

    for pp in alreadyUsedProperties:
        # print(pp.keys())
        results['already used'].append(list(pp.keys())[0])

    for pp in availableProperties:
        results['newly available'].append(list(pp.keys())[0])

    for pp, value in metadata.items():
        results['Metadata'].append(value['warning'])

    return results
