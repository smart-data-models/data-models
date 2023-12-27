# property check - PC
from utils.utils import *
from utils import *

propertyTypes = ["Property", "Relationship", "GeoProperty"]
incompleteDescription = "Incomplete description"
withoutDescription = "No description at all"
doubleDotsDescription = "Double dots in the middle"
wrongTypeDescription = "Wrong NGSI types"
missingTypeDescription = "Missing NGSI types"
exceptions = ["coordinates", "bbox", "type"]

def parse_yamlDict(yamlDict, datamodelRepoUrl, level):
    # TODO: import the function from python package by "from pysmartdatamodel.utils import *"
    attributes = set()

    output = {}
    if isinstance(yamlDict, list):
        for item in yamlDict:
            partialoutput = parse_yamlDict(item, datamodelRepoUrl, level+1)
            output = dict(output, **partialoutput)
    else:
        for prop in yamlDict:
            # print("prop ", prop)

            if prop == "id": continue

            if isinstance(yamlDict[prop], list) and len(yamlDict[prop]) > 1 and isinstance(yamlDict[prop][0], dict):
                for item in yamlDict[prop]:
                    partialoutput = parse_yamlDict(item, datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput)
    
            if isinstance(yamlDict[prop], dict):
                if prop in ["properties", "allOf", "oneOf", "anyOf", "items"]:
                    partialoutput = parse_yamlDict(yamlDict[prop], datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput)
                    continue
                # print("dict prop ", prop)
                propKeys = list(yamlDict[prop].keys())

                # if there's type, and there's no items, allOf, properties
                # if type is a 
                if isinstance(yamlDict[prop], dict) and prop != "x-ngsi" and not prop in exceptions:
                    # print("++++ context prop ", prop)
                    
                    try:
                        propertyType = yamlDict[prop]["x-ngsi"]["type"]
                        if propertyType in propertyTypes:
                            # print(propertyType)
                            # print(propertyTypes)
                            output[prop] = {}
                            output[prop]["x-ngsi"] = True
                            output[prop]["x-ngsi_text"] = "ok to " + str(propertyType)
                        else:
                            output[prop]["x-ngsi"] = False
                            output[prop]["x-ngsi_text"] = "Wrong NGSI type of " + propertyType + " in the description of the property on level " + str(level)
                    except:
                        output[prop] = {}
                        output[prop]["x-ngsi"] = False
                        output[prop]["x-ngsi_text"] = "Missing NGSI type of " + str(propertyTypes) + " in the description of the property on level " + str(level)

                    # checking the pure description
                    try:
                        description = yamlDict[prop]["description"]
                        if len(description) > 15:
                            # No double quotes in the middle
                            # if not (".." in description):
                                # If there is a link, check that the link is valid
                            output[prop]["documented"] = True
                            output[prop]["text"] = description
                            # else:
                            #     output[key]["documented"] = False
                            #     output[key]["text"] = doubleDotsDescription
                        else:
                            output[prop]["documented"] = False
                            output[prop]["text"] = incompleteDescription
                    except:
                        # output[key] = {}
                        output[prop]["documented"] = False
                        output[prop]["text"] = withoutDescription

                    # Type property matches data model name
                    if prop == "type" and level == 1:
                        try:
                            propertyType = yamlDict[prop]["enum"]
                            if propertyType[0] == extract_datamodel_from_repoUrl(datamodelRepoUrl):
                                output[prop]["type_specific"] = True
                                output[prop]["type_specific_text"] = "Type property matches to data model name on level " + str(level)
                            else:
                                output[prop]["type_specific"] = False
                                output[prop]["type_specific_text"] = "Type property doesn't match to data model name on level " + str(level)
                        except:
                            output[prop]["type_specific"] = False
                            output[prop]["type_specific_text"] = "Missing Type property"
                    
                    # duplicated attributes
                    if prop in attributes:
                        output[prop]["duplicated_prop"] = True
                        output[prop]["duplicated_prop_text"] = "Duplicated prop " + str(prop) + " on level " + str(level)
                    else:
                        attributes.add(prop)
                
                if "properties" in propKeys:
                    partialoutput = parse_yamlDict(yamlDict[prop]["properties"], datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput)
                if "items" in propKeys and yamlDict[prop]["items"]:
                    if isinstance(yamlDict[prop]["items"], list):
                        for index in range(len(yamlDict[prop]["items"])):
                            partialoutput = parse_yamlDict(yamlDict[prop]["items"][index], datamodelRepoUrl, level+1)
                            output = dict(output, **partialoutput)
                    else:
                        partialoutput = parse_yamlDict(yamlDict[prop]["items"], datamodelRepoUrl, level+1)
                        output = dict(output, **partialoutput)
                if "anyOf" in propKeys:
                    partialoutput = parse_yamlDict(yamlDict[prop]["anyOf"], datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput)
                if "allOf" in propKeys:
                    partialoutput = parse_yamlDict(yamlDict[prop]["allOf"], datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput)
                if "oneOf" in propKeys:
                    partialoutput = parse_yamlDict(yamlDict[prop]["oneOf"], datamodelRepoUrl, level+1)
                    output = dict(output, **partialoutput) 

    return output


def is_well_documented(output, yamlDict, datamodelRepoUrl):
    """
    Make summary for yamlDict
    """
    documented = "documentationStatusOfProperties"
    # echo("yamlDict", yamlDict)
    # output[documented] = {}
    output[documented] = parse_yamlDict(yamlDict, datamodelRepoUrl, 1)

    # for key in yamlDict:
    #     # print(key)
    #     # print(yamlDict[key])
    #     ################### warning ###################
    #     # this will fail wit any attribute defined through a oneOf, allOf or anyOf
    #     ################### warning ###################

    #     if key != "id":  # this will
    #         try:
    #             propertyType = yamlDict[key]["x-ngsi"]["type"]
    #             if propertyType in propertyTypes:
    #                 # print(propertyType)
    #                 # print(propertyTypes)
    #                 output[documented][key] = {}
    #                 output[documented][key]["x-ngsi"] = True
    #                 output[documented][key]["x-ngsi_text"] = "ok to " + str(propertyType)
    #             else:
    #                 output[documented][key]["x-ngsi"] = False
    #                 output[documented][key]["x-ngsi_text"] = "Wrong NGSI type of " + propertyType + " in the description of the property"
    #         except:
    #             output[documented][key] = {}
    #             output[documented][key]["x-ngsi"] = False
    #             output[documented][key]["x-ngsi_text"] = "Missing NGSI type of " + str(propertyTypes) + " in the description of the property"

    #         # checking the pure description
    #         try:
    #             description = yamlDict[key]["description"]
    #             if len(description) > 15:
    #                 # No double quotes in the middle
    #                 # if not (".." in description):
    #                     # If there is a link, check that the link is valid
    #                 output[documented][key]["documented"] = True
    #                 output[documented][key]["text"] = description
    #                 # else:
    #                 #     output[documented][key]["documented"] = False
    #                 #     output[documented][key]["text"] = doubleDotsDescription
    #             else:
    #                 output[documented][key]["documented"] = False
    #                 output[documented][key]["text"] = incompleteDescription
    #         except:
    #             # output[documented][key] = {}
    #             output[documented][key]["documented"] = False
    #             output[documented][key]["text"] = withoutDescription

        # # Type property matches data model name
        # if key == "type":
        #     try:
        #         propertyType = yamlDict[key]["enum"]
        #         if propertyType[0] == extract_datamodel_from_repoUrl(datamodelRepoUrl):
        #             output[documented][key]["type_specific"] = True
        #             output[documented][key]["type_specific_text"] = "Type property matches to data model name"
        #         else:
        #             output[documented][key]["type_specific"] = False
        #             output[documented][key]["type_specific_text"] = "Type property doesn't match to data model name"
        #     except:
        #         output[documented][key]["type_specific"] = False
        #         output[documented][key]["type_specific_text"] = "Missing Type property"
                
    allProperties = 0
    documentedProperties = 0
    faultyDescriptionProperties = 0
    notDescribedProperties = 0
    for key in output[documented]:
        allProperties += 1
        # print(output["properties"][key]["documented"])
        if output[documented][key]["documented"]:
            documentedProperties += 1
        elif output[documented][key]["text"] == incompleteDescription:
            faultyDescriptionProperties += 1
        elif output[documented][key]["text"] == withoutDescription:
            notDescribedProperties += 1

    output["schemaDiagnose"] = "This schema has " + str(allProperties) + " properties. " + str(notDescribedProperties) +" properties are not described at all and " + str(faultyDescriptionProperties) + " have descriptions that must be completed. " + str(allProperties - faultyDescriptionProperties - notDescribedProperties) + " are described but you can review them anyway. "

    return output







