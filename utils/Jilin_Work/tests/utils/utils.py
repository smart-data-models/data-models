import jsonref
import requests
import re
import datetime
import json
import yaml 

import jsonschema

from validator_collection import checkers
from jsonschema import validate, ValidationError, SchemaError, Draft202012Validator

propertyTypes = ["Property", "Relationship", "GeoProperty"]

TESTS = [
    "File Structure Check",
    "schema.json Content Check",
    "examples Check",
    "Others files Check"]

KEYWORDS_FOR_CERTAIN_CHECK = "smart-data-models"

CHECKED_PROPERTY_CASES = ['well documented', 'already used', 'newly available', 'Metadata', 'Failed']

json_output_dir = "/var/www/html/extra/mastercheck_output/"

SUFFIX = "mastercheck"

schema_json_yaml_dict = {}

exampleV2Output_filepath = None
exampleLDOutput_filepath = None

################################################
# Frontend message formats and functions related to message
# 
# Simple message formats are:
#   - starting, ending, under processing, loading, passed, failed, previous tests message...
# 
# Complex message formats are schema related, in order to give more concise info for contirbutors
################################################

newline = "\n  "
newsubline = "\n   "

mf_test_start = lambda jsonOutput, tz: f"Subject: {jsonOutput['subject']} Data Model: {jsonOutput['datamodel']} CHECK starts ... \n"
mf_test_end = lambda message: f"{message} \nPlease be reminded that the JSON output file will be temporarily stored FOR one hour. \n {''.join(['#']*30)}"
mf_test_basic = lambda testnumber, tz: f"{get_now_verbose(tz)} Test {testnumber} {TESTS[testnumber-1]}"
mf_test_processing = lambda subtestname, tz: f"{get_now_verbose(tz)} \t {subtestname} is processing ... \n"

mf_test_loading = lambda testnumber, tz: mf_test_basic(testnumber, tz) + " loading ...\n"
mf_test_passed = lambda testnumber, tz, message: mf_test_basic(testnumber, tz) + " passed!\n" + message + "\n"
mf_test_failed = lambda testnumber, tz, message: mf_test_basic(testnumber, tz) + " failed!\n" + message + "\n"
mf_test_previous= lambda testnumber: f"Previous Checked Tests - Test {testnumber} {TESTS[testnumber-1]}: "
mf_test_json = lambda jsonOutput, testnumber: f"<a href='{get_jsonoutput_url(jsonOutput, testnumber)}'>Please find the JSON data file for more detail.</a>\n\n"
mf_test_example_normalized = lambda exampleV2Output, exampleLDOutput: f"Systematically generated <a href='{get_normalized_examples_url(exampleV2Output)}'>example-normalized.json</a> and <a href='{get_normalized_examples_url(exampleV2Output)}'>example-normalized.json</a> \n\n"

def write_msg_to_file(message, mail):
    """
    Write message into the output file, which will display on the website

    Parameters:
        message (str): the return message
        mail (str): the mail of the user, used it to get the output file in
    """
    with open(json_output_dir + f"test_output_{mail}.txt", "a", newline="\n") as f:
        f.write(message)

def send_message(testnumber, mail, tz, type, jsonOutput=None, subtestname=""):
    """
    Create the message given different tests, types, and subtestname

    Parameters:
        testnumber (int): the number of test, 1 - file structure check, 2 - schema.json check, 
                        3 - examples check, 4 - other files check
        mail (str): the mail of the user
        tz : timezone
        type (str): the types of check processing, including: "start", "loading", "passed", "processing", 
                    "failed", "previous"
        jsonOutput (dict): the output dictionary for all tests
        subtestname (str): the name of the sub-test. In schema.json check, it includes property check and metadata check;
                            In examples check, it contains the checks for four types of example files

    """
    message = ""

    if type == "loading": # the return message when loading the check
        message = mf_test_loading(testnumber, tz)
    
    elif type == "passed": # the return message when the check passed
        
        global exampleV2Output_filepath, exampleLDOutput_filepath
        message = mf_test_passed(testnumber, tz, jsonOutput[testnumber]["message"])

        # generate the referral examples for examples-normalized.json and examples-normalized.jsonld files
        # if the examples check passed
        if exampleV2Output_filepath is not None and exampleLDOutput_filepath is not None:
            message += mf_test_example_normalized(exampleV2Output_filepath, exampleLDOutput_filepath)
            exampleV2Output_filepath, exampleLDOutput_filepath = None, None
        
        # generate the message contains the link to json output dictionary
        message += mf_test_json(jsonOutput, testnumber)
    
    elif type == "processing": # the return message when processing sub-tests
        message = mf_test_processing(subtestname, tz)
    
    elif type == "failed": # the return message when check failed
        
        if testnumber == 2:
            # 2 - schema.json check 
            message = mf_test_failed(testnumber, tz, jsonOutput[testnumber]["message"])
        else:
            # 3 - examples check
            message = mf_test_failed(testnumber, tz, jsonOutput[testnumber]["cause"])
        
        message += mf_test_json(jsonOutput, testnumber)
    
    elif type == "start": # the return message when check starts
        message = mf_test_start(jsonOutput, tz)
    
    elif type == "previous": 
        # the return message if the check has been done within one hour
        # and there are output files already
        # display the previous test details, and give the link
        for key in jsonOutput.keys():
            if key.isnumeric():
                message += mf_test_previous(int(key))
                message += mf_test_json(jsonOutput, int(key))
    
    else: # the return message when check ends
        message = mf_test_end(type)

    write_msg_to_file(message, mail)

def message_after_check_schema(output):
    """
    Generate a summary message based on the results of a schema validation check.

    Parameters:
    - output (dict): The summarized results from schema validation.

    Returns:
    - str: A message providing information about different property categories and metadata warnings.

    Example:
    >>> validation_results = {...}  # An example of summarized validation results
    >>> message_after_check_schema(validation_results)
    '
    These properties are well documented properties: 
    
        dateCreated, dateModified, source, name, ...

    These properties are already used properties: 
        
        openingHoursSpecification, startDate, ...

    No big issue with the named properties in general.
            
    Some warnings related to metadata:

    ...
    '

    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    results = output["sumup_results"]
    message = ""
    for key in CHECKED_PROPERTY_CASES[:-2]:
        if len(results[key]) != 0:
            msg = f"""
These properties are {key} properties: 
    {newline + ", ".join(results[key])}
"""
            message += msg

    if len(results[CHECKED_PROPERTY_CASES[-1]]) != 0:
        message += f"""
However, We highly suggest you to fix with these properties:

    {newline.join([" - "+text+newline+f"{', '.join(pps)}" for text, pps in results['Failed'].items()])}
        """
    else:
        message += f"""
No big issue with the named properties in general.
        """

    if len(results[CHECKED_PROPERTY_CASES[-2]]) != 0:
        message += f"""
Some warnings related to metadata:

    {newline.join([" - "+text for text in results['Metadata']])}
        """
    else:
        message += f"""
No warning with metadata.        
        """
    return message

def message_after_check_example(output):
    message = ""
    for _, pps in output["metadata"].items():
        if pps:
            msg = f"""

    {newline.join([" - "+text+newline+pp for text, pp in pps.items()])}
            """
            message += msg
    if not message:
        return f"""
No big issue with the metadata in /examples.
    """
    return message

def message_after_check(output, testnumber, isParamCheck=False):
    """
    Create return messages for parameters check, schema.json check
    """
    if isParamCheck:
        return output["cause"]
    if testnumber == 2:
        return message_after_check_schema(output)
    return ""

################################################
# Test output json file related:
# 
#       create, read, update, write json file, get json file url etc.
################################################

def create_output_json(testnumber, datamodelrepoUrl, mail, tz, metaSchema):
    """
    Create output json file for a specific check

    Parameters:
        testnumber (int): the number of test, 1 - file structure check, 2 - schema.json check, 
                        3 - examples check, 4 - other files check
        datamodelRepoUrl (str): the repository link to the data model
        mail (str): the mail of the user
        tz: timezone
        metaSchema (str): a link to metaSchema
    
    Returns:
        jsonOutput_filepath (str): the path of the output json file
        output (dict): the output json dictionary
    """
    subject = extract_subjectRaw_from_repoUrl(datamodelrepoUrl)
    datamodel = extract_datamodelRaw_from_repoUrl(datamodelrepoUrl)

    # create the path
    jsonOutput_filepath = json_output_dir + \
        f"{subject.strip('/').replace('/', '.')}_{datamodel.strip('/').replace('/', '.')}_{mail}_{get_now(tz)}_{SUFFIX}.json"
    
    try:
        # if path exists already, which means the previous checks exist
        # get the previous check return
        output = read_output_json(jsonOutput_filepath)
        output['lastModifiedTime'] = get_now_verbose(tz)

        send_message(testnumber, mail, tz, type="start", jsonOutput=output)
        send_message(testnumber, mail, tz, type="previous", jsonOutput=output)
        
    except FileNotFoundError:

        # create the metadata for json output
        output = {}
        output['subject'] = subject
        output['datamodel'] = datamodel
        output['mail'] = mail
        output['date'] = get_now(tz)
        output['repoUrl'] = datamodelrepoUrl
        output['createdTime'] = get_now_verbose(tz)
        output['lastModifiedTime'] = get_now_verbose(tz)
        output['metaschema'] = metaSchema
        output['message'] = ""

        send_message(testnumber, mail, tz, type="start", jsonOutput=output)
    
    # write the current output into the file
    update_output_json(jsonOutput_filepath, output)

    return jsonOutput_filepath, output
    
def read_output_json(jsonOutput_filepath):
    """
    Read the json output file
    """
    with open(jsonOutput_filepath, 'r') as file:
        output = json.load(file)
    return output

def update_output_json(jsonOutput_filepath, output):
    """
    Write the json output dictionary to the file
    """
    with open(jsonOutput_filepath, 'w') as file:
        json.dump(output, file)

def clean_test_data(jsonOutput_filepath, testnumber):
    """
    Clean up the previous test and update in json output
    """
    output = read_output_json(jsonOutput_filepath)
    output.pop(str(testnumber))
    update_output_json(jsonOutput_filepath, output)

def customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=True, isParamCheck=False):
    """
    Create the json output at the end of each check according to the status

    Parameters:
        output (dict): the json output of the specific check
        tz: timezone
        testnumber (int): the number of test, 1 - file structure check, 2 - schema.json check, 
                        3 - examples check, 4 - other files check
        jsonOutput_filepath (str): the file path to json output
        mail (str): the mail of the user
        flag (bool): whether check is passed or failed, True is passed and False is failed
        isParamCheck (bool): whether check is parameters check or not 
    """
    output["testnumber"] = testnumber
    output["testname"] = TESTS[testnumber-1]
    output["time"] = get_now_verbose(tz)
    
    # get the json output dictionary for all checks
    jsonOutput = read_output_json(jsonOutput_filepath)
    output['jsonUrl'] = get_jsonoutput_url(jsonOutput, testnumber)

    # if the check is passed, update the "result" in json output to True
    if flag:
        output["result"] = flag
    output["message"] = message_after_check(output, testnumber, isParamCheck)

    # update the json output with the information of the specific check
    jsonOutput[testnumber] = output
    jsonOutput["lastModifiedTime"] = get_now_verbose(tz)
    update_output_json(jsonOutput_filepath, jsonOutput)

    # create return message according to the status
    if flag:
        send_message(testnumber, mail, tz, type="passed", jsonOutput=jsonOutput)
    else:
        send_message(testnumber, mail, tz, type="failed", jsonOutput=jsonOutput)

def get_jsonoutput_url(jsonOutput, testnumber):
    """
    Generate the json output link
    """
    return f"https://smartdatamodels.org/extra/get_test_json_output.php?subject={jsonOutput['subject'].strip('/').replace('/', '.')}&datamodel={jsonOutput['datamodel'].strip('/').replace('/', '.')}&mail={jsonOutput['mail']}&date={jsonOutput['date']}&testnumber={testnumber}"

def get_normalized_examples_url(filePath):
    """
    Generate the referral normalized examples link
    """
    return f"https://smartdatamodels.org/extra/mastercheck_output/{filePath.split('/')[-1]}"

################################################
# Time related, two formats now
################################################
    
def get_now(tz, format="%m%d"):
    now = datetime.datetime.now(tz=tz)
    formatted_date = now.strftime(format) # MMDD
    return formatted_date

def get_now_verbose(tz, format="%Y-%m-%d %H:%M:%S"):
    return get_now(tz, format)

################################################
# To open json file when giving a url
################################################

def open_json(fileUrl):
    """
    TODO import the function from python package by "from pysmartdatamodel.utils import *"
    """
    import json
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            return json.loads(pointer.content.decode('utf-8'))
        except:
            return None

    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return json.loads(file.read())
        except:
            return None

def open_jsonref(fileUrl):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=False, merge_props=True) # 
            return output
        except:
            return ""
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read())
        except:
            print(fileUrl)
            return ""

################################################
# URL related
# 
#   - existance of url
#   - get existing urls
#   - create urls
#   - extract subject, data models information from urls
################################################
  
def is_url_existed(url, message=""):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    output = []
    try:
        pointer = requests.get(url)
        if pointer.status_code == 200:
            return [True, pointer.text]
        else:
            return [False, pointer.status_code]
    except:
        return [False, "wrong domain"]
    
def get_other_files_raw(repoUrl, checking_file):
    """
    Generate the other files link, such as notes.yaml
    """
    subjectRaw = extract_subjectRaw_from_repoUrl(repoUrl)
    datamodelRaw = extract_datamodelRaw_from_repoUrl(repoUrl)
    return f"https://raw.githubusercontent.com/{subjectRaw}/{datamodelRaw}/{checking_file}"
    
def get_context_jsonld_raw(repoUrl):
    """
    Generate the context.jsonld link in raw version

    TODO update the new context format
    """
    subjectRaw = extract_subjectRaw_from_repoUrl(repoUrl)
    return f"https://raw.githubusercontent.com/{subjectRaw}/master/context.jsonld"

def get_schema_json_raw(repoUrl):
    """
    Generate the schema.json link in raw version
    """
    subjectRaw = extract_subjectRaw_from_repoUrl(repoUrl)
    datamodelRaw = extract_datamodelRaw_from_repoUrl(repoUrl)
    schemaUrl = f"https://raw.githubusercontent.com/{subjectRaw}/{datamodelRaw}/schema.json"
    return schemaUrl

def create_example_url_raw(repoUrl, checking_file):
    """
    Generate the examples link in raw version
    """
    subjectRaw = extract_subjectRaw_from_repoUrl(repoUrl)
    datamodelRaw = extract_datamodelRaw_from_repoUrl(repoUrl)
    return f"https://raw.githubusercontent.com/{subjectRaw}/{datamodelRaw}/examples/{checking_file}"

# only in smart-data-models repo
# https://smart-data-models.github.io/subject/datamodel/schema.json
def create_schema_json_url(repoUrl):
    """
    Generate the schema.json link
    """
    subject = extract_subject_from_repoUrl(repoUrl)
    datamodel = extract_datamodel_from_repoUrl(repoUrl)
    return f"https://smart-data-models.github.io/{subject}/{datamodel}/schema.json"

def extract_string_from_url(repoUrl, left, right):
    """
    Extract string from url given the start and end
    """
    start = repoUrl.find(left) + len(left)
    end = repoUrl.find(right)
    return repoUrl[start:end]

def extract_subjectRaw_from_repoUrl(repoUrl):
    """
    Extract name of subject from repository url in raw version

    Examples:
    >>> extract_subjectRaw_from_repoUrl("https://github.com/smart-data-models/dataModel.Weather/tree/master/SeaConditions")
    "smart-data-models/dataModel.Weather"
    >>> extract_subjectRaw_from_repoUrl("https://github.com/smart-data-models/dataModel.Ports/tree/53f24ff86216be9ad01c04f9133141f50dc8920c/BoatAuthorized")
    "smart-data-models/dataModel.Ports"
    >>> extract_subjectRaw_from_repoUrl("https://github.com/smart-data-models/incubated/tree/master/CROSSSECTOR/DataSovereignty/AlgorithmAssessed")
    "smart-data-models/incubated"
    """
    if "/tree/" in repoUrl:
        return extract_string_from_url(repoUrl, "https://github.com/", "/tree/")
    elif "/blob/" in repoUrl:
        return extract_string_from_url(repoUrl, "https://github.com/", "/blob/")

def extract_datamodelRaw_from_repoUrl(repoUrl):
    """
    Extract name of data model from repository url in raw version

    Examples:
    >>> extract_datamodelRaw_from_repoUrl("https://github.com/smart-data-models/dataModel.Weather/tree/master/SeaConditions")
    "master/SeaConditions"
    >>> extract_datamodelRaw_from_repoUrl("https://github.com/smart-data-models/dataModel.Ports/tree/53f24ff86216be9ad01c04f9133141f50dc8920c/BoatAuthorized")
    "53f24ff86216be9ad01c04f9133141f50dc8920c/BoatAuthorized"
    >>> extract_datamodelRaw_from_repoUrl("https://github.com/smart-data-models/incubated/tree/master/CROSSSECTOR/DataSovereignty/AlgorithmAssessed")
    "CROSSSECTOR/DataSovereignty/AlgorithmAssessed"
    """
    if "/tree/" in repoUrl:
        start = repoUrl.find("/tree/") + len("/tree/")
    elif "/blob/" in repoUrl:
        start = repoUrl.find("/blob/") + len("/blob/")
    return repoUrl[start:]

def extract_subject_from_repoUrl(repoUrl):
    """
    Extract name of subject from repository url

    Examples:
    >>> extract_subject_from_repoUrl("https://github.com/smart-data-models/dataModel.Weather/tree/master/SeaConditions")
    "dataModel.Weather"
    >>> extract_subject_from_repoUrl("https://github.com/smart-data-models/dataModel.Ports/tree/53f24ff86216be9ad01c04f9133141f50dc8920c/BoatAuthorized")
    "dataModel.Ports"
    >>> extract_subject_from_repoUrl("https://github.com/smart-data-models/incubated/tree/master/CROSSSECTOR/DataSovereignty/AlgorithmAssessed")
    "incubated"
    """
    subjectRaw = extract_subjectRaw_from_repoUrl(repoUrl)
    return subjectRaw.strip('/').split('/')[-1]

def extract_datamodel_from_repoUrl(repoUrl):
    """
    Extract name of data model from repository url

    Examples:
    >>> extract_datamodel_from_repoUrl("https://github.com/smart-data-models/dataModel.Weather/tree/master/SeaConditions")
    "SeaConditions"
    >>> extract_datamodel_from_repoUrl("https://github.com/smart-data-models/dataModel.Ports/tree/53f24ff86216be9ad01c04f9133141f50dc8920c/BoatAuthorized")
    "BoatAuthorized"
    >>> extract_datamodel_from_repoUrl("https://github.com/smart-data-models/incubated/tree/master/CROSSSECTOR/DataSovereignty/AlgorithmAssessed")
    "AlgorithmAssessed"
    """
    datamodelRaw = extract_datamodelRaw_from_repoUrl(repoUrl)
    return datamodelRaw.strip('/').split('/')[-1]

################################################
# Payload parser
################################################
      
def parse_description(schemaPayload):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    output = {}
    purgedDescription = str(schemaPayload["description"]).replace(chr(34), "")
    # process the description
    purgedDescription = re.sub(r'\.([A-Z])', r'. \1', purgedDescription)
    
    separatedDescription = purgedDescription. split(". ")
    copiedDescription = list.copy(separatedDescription)
    
    for descriptionPiece in separatedDescription:
        if descriptionPiece in propertyTypes:
            output["type"] = descriptionPiece
            copiedDescription.remove(descriptionPiece)
        elif descriptionPiece.find("Model:") > -1:
            copiedDescription.remove(descriptionPiece)
            output["model"] = descriptionPiece.replace("'", "").replace(
                    "Model:", "")

        if descriptionPiece.find("Units:") > -1:
            copiedDescription.remove(descriptionPiece)
            output["units"] = descriptionPiece.replace("'", "").replace(
                    "Units:", "")
    description = ". ".join(copiedDescription)

    return output, description

def merge_duplicate_attributes(aa, bb):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    if bb:
        for key, values in bb.items():
            if key in aa:
                aa[key].extend(values)
            else:
                aa[key] = values
    return aa

def parse_payload_v2(schemaPayload, level):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    output = {}
    attributes = {level: []}
    if level == 1:
        if "allOf" in schemaPayload:
            for index in range(len(schemaPayload["allOf"])):
                if "definitions" in schemaPayload["allOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["allOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["allOf"][index], level + 1)
                    output = dict(output, **partialOutput)
                attributes = merge_duplicate_attributes(attributes, partialAttr)
        if "anyOf" in schemaPayload:
            for index in range(len(schemaPayload["anyOf"])):
                if "definitions" in schemaPayload["anyOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["anyOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["anyOf"][index], level + 1)
                    output = dict(output, **partialOutput)
                attributes = merge_duplicate_attributes(attributes, partialAttr)
        if "oneOf" in schemaPayload:
            for index in range(len(schemaPayload["oneOf"])):
                if "definitions" in schemaPayload["oneOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index]["definitions"], level + 1)
                    output = dict(output, **partialOutput)
                elif "properties" in schemaPayload["oneOf"][index]:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index], level + 1)
                    output = dict(output, **partialOutput["properties"])
                else:
                    partialOutput, partialAttr = parse_payload_v2(schemaPayload["oneOf"][index], level + 1)
                    output = dict(output, **partialOutput)
                attributes = merge_duplicate_attributes(attributes, partialAttr)

        if "properties" in schemaPayload:
            output, partialAttr = parse_payload_v2(schemaPayload["properties"], level + 1)
            attributes = merge_duplicate_attributes(attributes, partialAttr)
                
    elif level < 8:
        if isinstance(schemaPayload, dict):
            for subschema in schemaPayload:
                if subschema in ["allOf", "anyOf", "oneOf"]:
                    output[subschema] = []
                    for index in range(len(schemaPayload[subschema])):
                        if "properties" in schemaPayload[subschema][index]:
                            partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][index], level + 1)
                            output[subschema].append(partialOutput["properties"])
                        else:
                            partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][index], level + 1)
                            output[subschema].append(partialOutput)
                        attributes = merge_duplicate_attributes(attributes, partialAttr)

                elif subschema == "properties":
                    output[subschema] = {}
                    for prop in schemaPayload["properties"]:
                        try:
                            output[subschema][prop]
                        except:
                            output[subschema][prop] = {}
                            attributes[level].append(prop)
                        for item in list(schemaPayload["properties"][prop]):
                            if item in ["allOf", "anyOf", "oneOf"]:
                                output[subschema][prop][item] = []
                                for index in range(len(schemaPayload[subschema][prop][item])):
                                    partialOutput, partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item][index], level + 1)
                                    output[subschema][prop][item].append(partialOutput)
                                    attributes = merge_duplicate_attributes(attributes, partialAttr)
                            elif item == "description":
                                print("Detectada la descripcion de la propiedad=" + prop)
                                x_ngsi, description = parse_description(schemaPayload[subschema][prop])
                                output[subschema][prop][item] = description
                                if x_ngsi:
                                    output[subschema][prop]["x-ngsi"] = x_ngsi
                            
                            elif item == "items":
                                output[subschema][prop][item], partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item], level + 1)
                                attributes = merge_duplicate_attributes(attributes, partialAttr)
                            elif item == "properties":
                                output[subschema][prop][item], partialAttr = parse_payload_v2(schemaPayload[subschema][prop][item], level + 1)
                                attributes = merge_duplicate_attributes(attributes, partialAttr)
                            elif item == "type":
                                if schemaPayload[subschema][prop][item] == "integer":
                                    output[subschema][prop][item] = "number"
                                else:
                                    output[subschema][prop][item] = schemaPayload[subschema][prop][item]
                            else:
                                output[subschema][prop][item] = schemaPayload[subschema][prop][item]

                elif isinstance(schemaPayload[subschema], dict):        
                    attributes[level].append(subschema)     
                    output[subschema], partialAttr = parse_payload_v2(schemaPayload[subschema], level + 1)
                    attributes = merge_duplicate_attributes(attributes, partialAttr)
                else:
                    if subschema == "description":
                        x_ngsi, description = parse_description(schemaPayload)
                        output[subschema] = description
                        if x_ngsi:
                            output["x-ngsi"] = x_ngsi
                    else:
                        output[subschema] = schemaPayload[subschema]
        
        elif isinstance(schemaPayload, list):
            for index in range(len(schemaPayload)):
                partialOutput, partialAttr = parse_payload_v2(schemaPayload[index], level + 1)
                output = dict(output, **partialOutput)
                attributes = merge_duplicate_attributes(attributes, partialAttr)
    else:
        return None, None

    return output, attributes
    
################################################
# Convert a normalized json v2 file to key value format 
################################################

def normalized2keyvalues(normalizedPayload, output, tz, test, jsonOutput_filepath, mail):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    but has to customized a bit
    """
    normalizedDict = normalizedPayload
    # normalizedDict = json.loads(normalizedPayload)
    tmpoutput = {}
    # print(normalizedDict)
    for element in normalizedDict:
        # print(normalizedDict[element])
        try:
            value = normalizedDict[element]["value"]
            if isinstance(value, dict):
                tmpvalue = {}
                for key in value.keys():
                    tmpvalue[key] = value[key]["value"]
                tmpoutput[element] = tmpvalue
            else:
                tmpoutput[element] = value
        except:
            tmpoutput[element] = normalizedDict[element]
            output["cause"] = f"Convertion failed"
            output["time"] = str(datetime.datetime.now(tz=tz))
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False)
            return False

    # print(json.dumps(output, indent=4, sort_keys=True))
    return tmpoutput

def normalized2keyvalues_v2(normalizedPayload, output, tz, test, jsonOutput_filepath, mail, level=0):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    import json
    normalizedDict = normalizedPayload
    tmpoutput = {}
    for element in normalizedDict:
        try:
            prop = normalizedDict[element]
            if isinstance(prop, list) and len(prop) > 0 and isinstance(prop[0], dict):
                tmpList = []
                for idx in range(len(prop)):
                    suboutput = normalized2keyvalues_v2(prop[idx], output, tz, test, jsonOutput_filepath, mail, level+1)
                    if "type" in suboutput and "value" in suboutput:
                        tmpList.append(suboutput["value"])
                    else:
                        tmpList.append(suboutput)
                tmpoutput[element] = tmpList
            elif isinstance(prop, dict):
                if "@value" in prop:
                    tmpoutput[element] = prop["@value"]
                elif "value" in prop:
                    value = prop["value"]
                    if isinstance(value, dict):
                        # print(f"dict {element}")
                        tmpoutput[element] = normalized2keyvalues_v2({"value": value}, output, tz, test, jsonOutput_filepath, mail, level+1)["value"]
                    elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        # print(f"list {element}")
                        tmpList = []
                        for idx in range(len(value)):
                            if "type" in value[idx] and "value" in value[idx]: 
                                tmpList.append(normalized2keyvalues_v2(value[idx], output, tz, test, jsonOutput_filepath, mail, level+1)["value"])
                            else:
                                tmpList.append(normalized2keyvalues_v2(value[idx], output, tz, test, jsonOutput_filepath, mail, level+1))
                        tmpoutput[element] = tmpList
                    else:
                        tmpoutput[element] = value
                elif "object" in prop:
                    tmpoutput[element] = prop["object"]
                elif isinstance(prop, dict):
                    tmpoutput[element] = normalized2keyvalues_v2(prop, output, tz, test, jsonOutput_filepath, mail, level+1)
                else:
                    tmpoutput[element] = prop
            else:
                tmpoutput[element] = prop
        
        except:
            tmpoutput[element] = normalizedDict[element]
            output["cause"] = f"Convertion failed"
            output["time"] = str(datetime.datetime.now(tz=tz))
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False)
            return False
    
    return tmpoutput

def keyvalues2normalized_ld(keyvaluesPayload, yamlDict, detailed=True, level=0):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    import json

    def valid_date(datestring):
        import re
        from datetime import datetime, time

        if not ("T" in datestring) and ("Z" in datestring):
            try:
                time.fromisoformat(datestring.replace('Z', '+00:00'))
            except:
                return False, "Text"
            return True, "Time"

        else:
            date = datestring.split("T")[0]
            # print(date)
            try:
                validDate = re.match('^[0-9]{2,4}[-/][0-9]{2}[-/][0-9]{2,4}$', date)
                # print(validDate)
            except ValueError:
                return False, "Text"

            if validDate is not None:
                if len(datestring.split("T")) > 1:
                    return True, "DateTime"
                return True, "Date"
            else:
                return False, "Text"

    keyvaluesDict = keyvaluesPayload
    output = {}
    # print(normalizedDict)
    for element in keyvaluesDict:
        if level == 0 and element in ["id", "type", "@context"]: continue
        item = {}
        if isinstance(keyvaluesDict[element], list):
            # it is an array
            item["type"] = yamlDict[element]['x-ngsi']['type']
            if detailed:
                if len(keyvaluesDict[element]) > 0 and isinstance(keyvaluesDict[element][0], dict):
                    tmpList = []
                    for idx in range(len(keyvaluesDict[element])):
                        tmpList.append(keyvalues2normalized_ld(keyvaluesDict[element][idx], yamlDict[element][idx], level=level+1))
                    item["value"] = tmpList
                else:
                    item["value"] = keyvaluesDict[element]
            else:
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], dict):
            # it is an object
            # item["type"] = "object"
            if element == "location":
                item["type"] = yamlDict[element]['x-ngsi']['type']
            elif "type" in keyvaluesDict[element] and "coordinates" in keyvaluesDict[element]: # location-like property
                item["type"] = yamlDict[element]['x-ngsi']['type']
            else:
                item["type"] = yamlDict[element]['x-ngsi']['type']
            if detailed:
                item["value"] = keyvalues2normalized_ld(keyvaluesDict[element], yamlDict[element], level=level+1)
            else:
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], str):
            dateFlag, dateType = valid_date(keyvaluesDict[element])
            if dateFlag:
                # it is a date
                item["type"] = yamlDict[element]['x-ngsi']['type']
                if dateType == "Date": 
                    item["value"] = {"@type": "Date", "@value": keyvaluesDict[element]}
                elif dateType == "Time": 
                    item["value"] = {"@type": "Time", "@value": keyvaluesDict[element]}
                else:
                    item["value"] = {"@type": "DateTime", "@value": keyvaluesDict[element]}
            else:
            # it is a string
                item["type"] = yamlDict[element]['x-ngsi']['type']
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], int) or isinstance(keyvaluesDict[element], float):
            # it is an number
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = keyvaluesDict[element]
        elif keyvaluesDict[element] == True:
            # it is an boolean
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = json.loads("true")
        elif keyvaluesDict[element] == False:
            # it is an boolean
            item["type"] = yamlDict[element]['x-ngsi']['type']
            item["value"] = json.loads("false")
        else:
            print("*** other type ***")
            print("I do not know what is it")
            print(keyvaluesDict[element])
            print("--- other type ---")
        output[element] = item

    if "id" in keyvaluesDict:
        output["id"] = keyvaluesDict["id"]
    if "type" in keyvaluesDict:
        output["type"] = keyvaluesDict["type"]
    if "@context" in keyvaluesDict:
        output["@context"] = keyvaluesDict["@context"]
    
    return output


def keyvalues2normalized_v2(keyvaluesPayload, detailed=True):
    """
    TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    """
    import json

    def valid_date(datestring):
        import re
        date = datestring.split("T")[0]
        # print(date)
        try:
            validDate = re.match('^[0-9]{2,4}[-/][0-9]{2}[-/][0-9]{2,4}$', date)
            # print(validDate)
        except ValueError:
            return False

        if validDate is not None:
            return True
        else:
            return False

    keyvaluesDict = keyvaluesPayload
    output = {}
    # print(normalizedDict)
    for element in keyvaluesDict:
        item = {}
        if isinstance(keyvaluesDict[element], list):
            # it is an array
            # item["type"] = "array"
            item["type"] = "StructuredValue"
            if detailed:
                if len(keyvaluesDict[element]) > 0 and isinstance(keyvaluesDict[element][0], dict):
                    tmpList = []
                    for idx in range(len(keyvaluesDict[element])):
                        tmpList.append(keyvalues2normalized_v2(keyvaluesDict[element][idx]))
                    item["value"] = tmpList
                else:
                    item["value"] = keyvaluesDict[element]
            else:
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], dict):
            # it is an object
            # item["type"] = "object"
            if element == "location":
                item["type"] = "geo:json"
            else:
                item["type"] = "StructuredValue"
            if detailed:
                item["value"] = keyvalues2normalized_v2(keyvaluesDict[element])
            else:
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], str):
            if valid_date(keyvaluesDict[element]):
                # it is a date
                # item["format"] = "date-time"
                item["type"] = "DateTime"
            else:
            # it is a string
                # item["type"] = "string"
                item["type"] = "Text"
            item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], int) or isinstance(keyvaluesDict[element], float):
            # it is an number
            # item["type"] = "number"
            item["type"] = "Number"
            item["value"] = keyvaluesDict[element]
        elif keyvaluesDict[element] == True:
            # it is an boolean
            # item["type"] = "boolean"
            item["type"] = "Boolean"
            item["value"] = json.loads("true")
        elif keyvaluesDict[element] == False:
            # it is an boolean
            # item["type"] = "boolean"
            item["type"] = "Boolean"
            item["value"] = json.loads("false")
        else:
            print("*** other type ***")
            print("I do now know what is it")
            print(keyvaluesDict[element])
            print("--- other type ---")
        output[element] = item

    if "id" in output:
        output["id"] = output["id"]["value"]
    if "type" in output:
        output["type"] = output["type"]["value"]
    if "@context" in output:
        output["@context"] = output["@context"]["value"]
    
    return output


################################################
# Check key-value and normalized format
################################################

def check_keyvalue(payload):
    """
    Check the key-value format of examples.

    Parameters:
        payload (dict): the payload of examples
    
    Returns:
        Tuple((str, list), bool): return an empty list with bool True if the check passed
                                return a list of failed properties with bool False if the check failed
                                return a string 'Unable to read' with bool False if the payload is wrong
    """
    props = []
    try:
        for prop, item in payload.items():
            if isinstance(item, dict):
                if "type" in item.keys() and "value" in item.keys():
                    props.append(prop)
        if len(props) == 0:
            return props, True
        else:
            return props, False
    except:
        return 'Unable to read', False
    

def check_normalized(payload):
    """
    Check the normalized format of examples.

    Parameters:
        payload (dict): the payload of examples
    
    Returns:
        Tuple((str, list), bool): return an empty list with bool True if the check passed
                                return a list of failed properties with bool False if the check failed
                                return a string 'Unable to read' with bool False if the payload is wrong
    """
    props = []
    try:
        for prop, item in payload.items():
            if prop in ['id', 'type', '@context']: continue
            if not isinstance(item, dict):
                props.append(prop)
            else:
                if not "type" in item.keys():
                    props.append(prop)
                    
                if (not "value" in item.keys()) and (not "object" in item.keys()):
                    props.append(prop)
        
        if len(props) == 0:
            return props, True
        else:
            return props, False
    except:
        return 'Unable to read', False

################################################
# parameters check related
################################################

def check_parameters(output, tz, jsonOutput_filepath, schemaUrl="", mail="", test="", metaSchema="", tag="", additionalProperties=False):

    # check schemaUrl
    if schemaUrl:
        # validate inputs
        existsSchema = is_url_existed(schemaUrl)
        
        # url provided is an existing url
        if not existsSchema[0]:
            output["cause"] = f"Cannot find the {tag} at " + schemaUrl
            output["time"] = str(datetime.datetime.now(tz=tz))
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False

        # url is actually a json
        try:
            schemaDict = json.loads(existsSchema[1])
        except ValueError:
            output["cause"] = f"{tag} " + schemaUrl + " is not a valid json"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False
        
        # test that it is a valid schema against the metaschema
        try:
            schema = open_jsonref(schemaUrl)
            # echo("len of schema", len(str(schema)))
            # echo("schema", schema)
            if not bool(schema):
                output["cause"] = f"json {tag} returned empty (wrong $ref?)"
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
        except:
            output["cause"] = f"json {tag} cannot be fully loaded"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False

        try:
            yamlDict, attributes = parse_payload_v2(schema, 1)
            global schema_json_yaml_dict
            if tag == "schema": schema_json_yaml_dict = yamlDict.copy()
        except:
            output["cause"] = f"{tag} cannot be loaded (possibly invalid $ref)"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False
    
        # check the duplicated attributes
        if tag == "schema" and len(attributes[2]) != len(set(attributes[2])):

            def find_duplicates(input_list):
                """
                Find and output the duplicated values inside a list.
                Args:
                    input_list (list): The list to search for duplicates in.
                Returns:
                    list: A list containing the duplicated values found in the input list.
                """
                seen = set()
                duplicates = set()

                for item in input_list:
                    if item in seen:
                        duplicates.add(item)
                    else:
                        seen.add(item)

                return list(duplicates)

            output["cause"] = f"Duplicated attributes (User-defined properties is duplicated with system-defined properties):\n\t{', '.join(find_duplicates(attributes[2]))}"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False


        # key-value and normalized format checking
        if not "normalized.json" in schemaUrl:
            # key-value
            props, flag = check_keyvalue(schema)
            if isinstance(props, str):
                output["cause"] = f"{props} in {schemaUrl.split('/')[-1]}."
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
            else:
                if not flag:
                    output["cause"] = f"{', '.join(props)} should be in key-value format"
                    output["time"] = str(datetime.datetime.now(tz=tz))
                    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                    customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                    return False
        else:
            # normalized format
            props, flag = check_normalized(schema)
            if isinstance(props, str):
                output["cause"] = f"{props} in {schemaUrl.split('/')[-1]}."
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
            else:
                if not flag:
                    output["cause"] = f"{', '.join(props)} should be in normalized format, can be caused by missing `type` or missing `value` or `object`"
                    output["time"] = str(datetime.datetime.now(tz=tz))
                    output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                    customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                    return False

        
        if schemaUrl.endswith("schema.json"):
            try: 
                validate(instance=schema, schema=metaSchema, format_checker=Draft202012Validator.FORMAT_CHECKER)
            except jsonschema.exceptions.ValidationError as err:
                # print(err)
                output["cause"] = f"{tag} does not validate as a json schema"
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                output["errorSchema"] = str(err)
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
        else:
            try:
                # Add additionalProperties
                if not additionalProperties:
                    # tmpSchema = {}
                    # tmpSchema["type"] = "object"
                    # tmpSchema["properties"] = {}
                    # for idx in range(len(metaSchema["allOf"])):
                    #     tmpSchema["properties"] = dict(tmpSchema["properties"], **metaSchema["allOf"][idx]["properties"])
                    # tmpSchema["additionalProperties"] = False
                    # metaSchema["allOf"] = [tmpSchema]

                    def flatten_allOf(schema):
                        tmpSchema = {}
                        tmpSchema["properties"] = {}
                        for idx in range(len(schema["allOf"])):
                            if "allOf" in schema["allOf"][idx]:
                                tmpOutput = flatten_allOf(schema["allOf"][idx])
                                tmpSchema["properties"] = dict(tmpSchema["properties"], **tmpOutput["properties"])
                            if "properties" in schema["allOf"][idx]:
                                tmpSchema["properties"] = dict(tmpSchema["properties"], **schema["allOf"][idx]["properties"])
                        return tmpSchema

                    if "allOf" in metaSchema:
                        tmpSchema = flatten_allOf(metaSchema)
                        tmpSchema["additionalProperties"] = False
                        metaSchema["allOf"] = [tmpSchema]
                    elif "properties" in metaSchema:
                        metaSchema["additionalProperties"] = False

                if "example-normalized" in schemaUrl:
                    result = normalized2keyvalues_v2(schema, output, tz, test, jsonOutput_filepath, mail)

                    if not result:
                        return result
                    schema = result
                
                if "@context" in schema:
                    schema.pop("@context")

                validate(instance=schema, schema=metaSchema, format_checker=Draft202012Validator.FORMAT_CHECKER)
            except jsonschema.exceptions.ValidationError as err:
                # print(err)
                spacer = '\n'
                output["cause"] = f"{tag} does not validate as a json schema. {str(err).split(spacer)[0]}"
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                output["errorSchema"] = str(err)
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
            except SchemaError as err:
                spacer = '\n'
                output["cause"] = f"schema.json error while validating the {tag}. {str(err).split(spacer)[0]}"
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                output["errorSchema"] = str(err)
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
            except Exception as err:
                spacer = '\n'
                output["cause"] = f"Exception occurs while validating the {tag}. {str(err).split(spacer)[0]}"
                output["time"] = str(datetime.datetime.now(tz=tz))
                output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
                output["errorSchema"] = str(err)
                customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
                return False
        
    # check email
    if mail:
        # mail is a real email
        if not checkers.is_email(mail):
            output["cause"] = "mail " + mail + " is not a valid email"
            output["time"] = str(datetime.datetime.now(tz=tz))
            output["parameters"] = {"schemaUrl": schemaUrl, "mail": mail, "test": test}
            customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
            return False
    
    return output, schemaDict, yamlDict



def is_valid_yaml(output, tz, jsonOutput_filepath, yamlUrl="", mail="", test="", tag=""):
    """
    Process the model.yaml file
    """
    existsYaml = is_url_existed(yamlUrl)
        
    # url provided is an existing url
    if not existsYaml[0]:
        output["cause"] = f"Cannot find the {tag} at " + yamlUrl
        output["time"] = str(datetime.datetime.now(tz=tz))
        customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
        return False

    # url is actually a json
    try:
        yamlDict = yaml.safe_load(existsYaml[1])
    except ValueError:
        output["cause"] = f"{tag} " + yamlUrl + " is not a valid json"
        output["time"] = str(datetime.datetime.now(tz=tz))
        output["parameters"] = {"schemaUrl": yamlUrl, "mail": mail, "test": test}
        customized_json_dumps(output, tz, test, jsonOutput_filepath, mail, flag=False, isParamCheck=True)
        return False
    
    return output, yamlDict


################################################
# generate examples for referral
################################################

def generate_examples(exampleV2NormalizedUrl, exampleLDNormalizedUrl, output, tz, test, jsonOutput_filepath, mail):
    """
    Generate the referral examples
    """
    
    global schema_json_yaml_dict, exampleV2Output_filepath, exampleLDOutput_filepath

    baseV2Normalized = open_json(exampleV2NormalizedUrl)
    baseLDNormalized = open_json(exampleLDNormalizedUrl)

    # convert normalized format into key-value format and then convert it back
    # in order to get the correct type for ngsi-v2
    exampleNL2KV = normalized2keyvalues_v2(baseV2Normalized, output, tz, test, jsonOutput_filepath, mail)
    exampleV2Normalized = keyvalues2normalized_v2(exampleNL2KV, detailed=False)
    # convert normalized format into key-value format and then convert it back
    # in order to get the correct type for ngsi-ld
    exampleNL2KV = normalized2keyvalues_v2(baseLDNormalized, output, tz, test, jsonOutput_filepath, mail)
    exampleLDNormalized = keyvalues2normalized_ld(exampleNL2KV, schema_json_yaml_dict, detailed=False)
    
    exampleV2Output_filepath = jsonOutput_filepath.replace(".json", "_example-normalized.json")
    exampleLDOutput_filepath = jsonOutput_filepath.replace(".json", "_example-normalized.jsonld")

    update_output_json(exampleV2Output_filepath, exampleV2Normalized)
    update_output_json(exampleLDOutput_filepath, exampleLDNormalized)


