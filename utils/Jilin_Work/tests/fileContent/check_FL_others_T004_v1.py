# FL stands for inside file check for one data model
# this python file is focused on other files
# like notes.yaml, ADOPTERS.yaml, CONTRIBUTORS.yaml, LICENSE.md

from utils.utils import *

CHECK_OTHERS = [
    "notes.yaml",
    "ADOPTERS.yaml",
    ]

def check_FL_others(datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath):
    """
    Check other files given the data model link
    """

    send_message(testnumber, mail, tz, type="loading")

    output = {"result": False}  # the json answering the test

    # go through all the files
    for checking_file in CHECK_OTHERS:
        fileUrl = get_other_files_raw(datamodelRepoUrl, checking_file)
        
        # check whether yaml file is valid
        cfoutput = {}
        result =  is_valid_yaml(cfoutput, tz, jsonOutput_filepath, yamlUrl=fileUrl, mail=mail, test=testnumber, tag="yamls")
        
        if not result:
            return result
    
        cfoutput, yamlDict = result
        send_message(testnumber, mail, tz, type="processing", jsonOutput=None, subtestname=f"{checking_file} check")
        
        # TODO: check there's an email in the ADOPTERS.yaml file

    customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail)    

    return True
