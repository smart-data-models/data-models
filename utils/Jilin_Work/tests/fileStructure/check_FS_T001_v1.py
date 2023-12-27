# Stands for check physical structure of one data model
# which is to check: 
#       - File exists
#       - File type correct
#       - Name correctly
# 
#  Least acceptable (LA) data model structure is as follows:
#   /
#       - examples/
#           - example-normalized.json or example-normalized.jsonId
#       - schema.json
# 
#  Other cases: general accepatble data model, and complete data model structure (CM)


import datetime
import json
import sys

from utils.utils import *

# url: check whether return 200
def check_FS_minimal(fileUrl, tz, testnumber, mail, jsonOutput_filepath):
    """
    Check the file structure to meet the minimal requirements
        - examples/
            - example-normalized.json or example-normalized.jsonId
        - schema.json
    """

    output = {"result": False}  # the json answering the test

    examples = is_url_existed(fileUrl+"/examples", "exmaples")[0]
    schemaJson = is_url_existed(fileUrl+"/schema.json", "schema.json")[0]
    normalizedJson = is_url_existed(fileUrl+"/examples/example-normalized.json", "example-normalized.json")[0]
    normalizedJsonld = is_url_existed(fileUrl+"/examples/example-normalized.jsonld", "example-normalized.jsonld")[0]
    
    if not examples:
        output["cause"] = f"{fileUrl.split('/')[-1]} Missing examples folder: Cannot open the url at " + fileUrl+"/examples"
        output["time"] = str(datetime.datetime.now(tz=tz))
        customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=False)
        
        return False
    
    if not schemaJson:
        output["cause"] = f"{fileUrl.split('/')[-1]} Missing schema.json: Cannot open the url at " + fileUrl+"/schema.json"
        output["time"] = str(datetime.datetime.now(tz=tz))
        customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=False)
        
        return False
    
    if not (normalizedJson | normalizedJsonld):
        output["cause"] = f"{fileUrl.split('/')[-1]} Missing example-normalized.json or example-normalized.jsonld: at least one is a must"
        output["time"] = str(datetime.datetime.now(tz=tz))
        customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail, flag=False)
        
        return False

    customized_json_dumps(output, tz, testnumber, jsonOutput_filepath, mail)
    
    return True

def check_FS_nomral():
    """
    Check the file structure to meet the normal requirements
        - examples/
            - example.json
            - example.jsonld
            - example-normalized.json
            - example-normalized.jsonId
        - schema.json
    """
    pass

def check_FS_full():
    """
    Check the file structure to meet the full requirements
        - examples/
            - example.json
            - example.jsonld
            - example-normalized.json
            - example-normalized.jsonId
        - schema.json
        - ADOPTERS.yaml
        - notes.yaml
    """
    pass


def check_fileStructure(fileUrl, tz, testnumber, mail, jsonOutput_filepath, type="minimal"):
    """
    Check the file structure
    """

    send_message(testnumber, mail, tz, type="loading")
    
    if type == "minimal":
        return check_FS_minimal(fileUrl, tz, testnumber, mail, jsonOutput_filepath)
    elif type == "normal":
        return check_FS_nomral(fileUrl, tz, testnumber, mail, jsonOutput_filepath)
    elif type == "full":
        return check_FS_full(fileUrl, tz, testnumber, mail, jsonOutput_filepath)


