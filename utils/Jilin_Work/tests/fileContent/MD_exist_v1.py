# Check whether the metadata exists in schema.json and examples
# schema.json: $id, title, $schema, $schemaVersion, modelTag, description, required
# id, type, @context

from validator_collection import checkers
from utils.utils import *

import sys
import datetime
import json
import jsonschema

################################################
# Metadata in examples: id, type, @context
################################################

def check_id(output, jsonDict):
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "id" in jsonDict:
            id = jsonDict["id"]
            if id == "":
                output["metadata"]["id"] = {"warning": "id is empty"}
            elif not isinstance(id, str):
                output["metadata"]["id"] = {"warning": "id is not a string"}
        else:
            output["metadata"]["id"] = {"warning": "Missing id clause, include id = '' in the header"}
    except:
        output["metadata"]["id"] = {"warning": "not possible to check id clause, Does it exist a id = '' in the header?"}
    
    return output

def check_type(output, jsonDict, repoUrl):
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "type" in jsonDict:
            type = jsonDict["type"]
            if type == "":
                output["metadata"]["type"] = {"warning": "type is empty"}
            elif not isinstance(type, str):
                output["metadata"]["type"] = {"warning": "type is not a string"}
            elif type != extract_datamodel_from_repoUrl(repoUrl):
                output["metadata"]["type"] = {"warning": f"type {type} doesn't match the datamodel {extract_datamodel_from_repoUrl(repoUrl)}, please check it again"}
        else:
            output["metadata"]["type"] = {"warning": "Missing type clause, include type = '' in the header"}
    except:
        output["metadata"]["type"] = {"warning": "not possible to check type clause, Does it exist a type = '' in the header?"}

    return output

def check_at_context(output, jsonDict, repoUrl):
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "@context" in jsonDict:
            context = jsonDict["@context"]
            if len(context) == 0:
                output["metadata"]["@context"] = {"warning": "@context is an empty list or is empty"}
            else:
                for url in context:
                    if not is_url_existed(url)[0]:
                        output["metadata"]["@context"] = {"warning": f"{url} in @context is not reachable, please check it again"}
            if (KEYWORDS_FOR_CERTAIN_CHECK in repoUrl) and (not "@context" in output["metadata"].keys()):
                if not (get_context_jsonld_raw(repoUrl) in context):
                    output["metadata"]["@context"] = {"warning": "@context doesn't include the right context link, please check it again or ignore this message if it's an unpublished datamodel"}
        else:
            output["metadata"]["@context"] = {"warning": "Missing @context clause, include @context = '' in the header"}
    except:
        output["metadata"]["@context"] = {"warning": "not possible to check @context clause, Does it exist a @context = '' in the header?"}

    return output
    

metadata_check = {
    "id": lambda output, jsonDict, repoUrl: check_id(output, jsonDict),
    "type": lambda output, jsonDict, repoUrl: check_type(output, jsonDict, repoUrl),
    "@context": lambda output, jsonDict, repoUrl: check_at_context(output, jsonDict, repoUrl),
}

def is_metadata_existed_examples(output, jsonDict, repoUrl, message="", checklist=["id", "type", "@context"]):

        # check "id", "type", "@context"
    for checkpoint in checklist:
        if checkpoint in metadata_check:
            check_func = metadata_check[checkpoint]
            output = check_func(output, jsonDict, repoUrl)

    return output


################################################
# Metadata in examples: id, type, @context
################################################

# TODO: import the function from python package by "from pysmartdatamodel.utils import *"

def is_metadata_existed(output, jsonDict, repoUrl, message="", checkall=True, checklist=None):

    # if checkall is True, then ignore checklist
    # if checkall is False, then checklist will be used

    # if not checkall:
        # ["$schema", "$id", "title", "", "description", "tags", "version", "required clause"]

    # check that the "$schema" exist, by default is "http://json-schema.org/schema"
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$schema" in jsonDict:
            schema = jsonDict["$schema"]
            if schema == "":
                output["metadata"]["$schema"] = {"warning": "$schema is empty"}
            elif not isinstance(schema, str):
                output["metadata"]["$schema"] = {"warning": "$schema is not a string"}
            # 
            elif schema != "http://json-schema.org/schema#":
                output["metadata"]["$schema"] = {"warning": "$schema should be \"http://json-schema.org/schema#\" by default"}
        else:
            output["metadata"]["$schema"] = {"warning": "Missing $schema clause, include $schema = '' in the header"}
    except:
        output["metadata"]["$schema"] = {"warning": "not possible to check $schema clause, Does it exist a $schema = '' in the header?"}

    # check that the "$id" exist
    try:
        # print(jsonDict)
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$id" in jsonDict:
            # print("-----------")
            id = jsonDict["$id"]
            if id == "":
                output["metadata"]["$id"] = {"warning": "$id is empty"}
            elif not isinstance(id, str):
                output["metadata"]["$id"] = {"warning": "$id is not a string"}
            # https://smart-data-models.github.io/dataModel.DataQuality/DataQualityAssessment/schema.json
            elif (KEYWORDS_FOR_CERTAIN_CHECK in repoUrl) and (id != create_schema_json_url(repoUrl)):
                output["metadata"]["$id"] = {"warning": "$id doesn't match, please check it again or ignore this message if it's an unpublished datamodel"}
        else:
            output["metadata"]["$id"] = {"warning": "Missing $id clause, include $id = '' in the header"}
    except:
        output["metadata"]["$id"] = {"warning": "not possible to check $id clause, Does it exist a $id = '' in the header?"}
    
    # check that the title exist
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "title" in jsonDict:
            title = jsonDict["title"]
            if title == "":
                output["metadata"]["title"] = {"warning": "Title is empty"}
            elif not isinstance(title, str):
                output["metadata"]["title"] = {"warning": "Title is not a string"}
            elif len(title) < 15:
                output["metadata"]["title"] = {"warning": "Title too short"}
        else:
            output["metadata"]["title"] = {"warning": "Missing title clause, include title = '' in the header"}
    except:
        output["metadata"]["title"] = {"warning": "not possible to check title clause, Does it exist a title = '' in the header?"}

    # check that the description exists
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "description" in jsonDict:
            description = jsonDict["description"]
            if description == "":
                output["metadata"]["description"] = {"warning": "Description is empty"}
            elif not isinstance(description, str):
                output["metadata"]["description"] = {"warning": "Description is not a string"}
            elif len(description) < 34:
                output["metadata"]["description"] = {"warning": "Description is too short"}
        else:
            output["metadata"]["description"] = {"warning": "Missing description clause, include description = '' in the header"}
    except:
        output["metadata"]["description"] = {"warning": "not possible to check description clause, does it exist a description = '' in the header?"}

    # check that the tags exist
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "modelTags" in jsonDict:
            modelTags = jsonDict["modelTags"]
            if modelTags == "":
                output["metadata"]["modelTags"] = {"warning": "modelTags is empty"}
            elif not isinstance(title, str):
                output["metadata"]["modelTags"] = {"warning": "modelTags is not a string"}
        else:
            output["metadata"]["modelTags"] = {"warning": "Missing modelTags clause, , include modelTags = '' in the header"}
    except:
        output["metadata"]["modelTags"] = {"warning": "not possible to check modelTags clause, does it exit a modelTags = '' in the header?"}

    # check that the version exists
    try:
        import re
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "$schemaVersion" in jsonDict:
            schemaVersion = jsonDict["$schemaVersion"]
            pattern = "^\d{1,3}.\d{1,3}.\d{1,3}$"
            if schemaVersion == "":
                output["metadata"]["schemaVersion"] = {"warning": "missing $schemaVersion, include the value. Default = 0.0.1"}
            elif not isinstance(schemaVersion, str):
                output["metadata"]["schemaVersion"] = {"warning": "$schemaVersion is not a string"}
            elif re.search(pattern, schemaVersion) is None:
                output["metadata"]["schemaVersion"] = {"warning": "Schema version format wrong. Right is x.x.x"}
        else:
            output["metadata"]["schemaVersion"] = {"warning": "Missing schemaVersion clause, include $schemaVersion = '' in the header "}
    except:
        output["metadata"]["schemaVersion"] = {"warning": "not possible to check schemaVersion clause, does it exist a $schemaVersion = '' in the header?"}

    # check that the required clause exists
    try:
        metadata = "metadata"
        if "metadata" not in output:
            output[metadata] = {}
        if "required" in jsonDict:
            required = jsonDict["required"]
            # print(required)
            # print(type(required))
            if required == "":
                output["metadata"]["required"] = {"warning": "missing required, include the values. Default = ['id', 'type]"}
            elif not isinstance(required, list):
                output["metadata"]["required"] = {"warning": "required is not a list"}
            elif ("id" not in required) or ("type" not in required):
                output["metadata"]["required"] = {"warning": "id and type are mandatory"}
            elif len(required) > 4:
                output["metadata"]["required"] = {"warning": "Too many required attributes, consider its reduction to less than 5 preferably just id and type"}
        else:
            output["metadata"]["required"] = {"warning": "Missing required clause, include required = ['id', 'type']"}
    except:
        output["metadata"]["required"] = {"warning": "not possible to check required clause, does it exist a required = ['id', 'type']?"}

    return output
