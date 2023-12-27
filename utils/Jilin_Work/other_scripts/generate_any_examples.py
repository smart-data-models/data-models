# this file create the examples from a list of schemas in a directory with the name of the data model
import os
import json
from os import listdir
from os.path import isfile, join


def open_json(fileUrl):
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


def keyvalues2normalized_v2(keyvaluesPayload, detailed=True):
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
            elif "type" in keyvaluesDict[element] and "coordinates" in keyvaluesDict[element]: # location-like property
                item["type"] = "geo:json"
            else:
                item["type"] = "StructuredValue"
            if detailed:
                item["value"] = keyvalues2normalized_v2(keyvaluesDict[element])
            else:
                item["value"] = keyvaluesDict[element]
        elif isinstance(keyvaluesDict[element], str):
            dateFlag, dateType = valid_date(keyvaluesDict[element])
            if dateFlag:
                # it is a date
                # item["format"] = "date-time"
                item["type"] = "DateTime"
            else:
            # it is a string
                # item["type"] = "string"
                item["type"] = dateType
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
            print("I do not know what is it")
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


mypath = "."

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files = [i for i in onlyfiles if i[0] != "_"]
print(files)
counter = 0
limit = 1000
exceptions = []

for file in files:
    dataModel = file.split(".")[0]
    print(dataModel)
    if dataModel not in exceptions and counter < limit:
        counter += 1
        # generate NGSI-LD normalized
        # generate NGSI-LD kevalues
        # generate NGSIv2 keyvalues
        # generate NGSI

        # TODO Remember to change the schema.json file path
        origin = "https://raw.githubusercontent.com/smart-data-models/incubated/master/OCF/" + dataModel + "/schema.json "
        
        callNGSILDNormalized = "https://smartdatamodels.org/extra/ngsi-ld_generator.php?schemaUrl=" + origin + "&email=alberto.abella@fiware.org"
        callNGSILDKeyvalues = "https://smartdatamodels.org/extra/ngsi-ld_generator_keyvalues_v0.95.php?schemaUrl=" + origin + "&email=alberto.abella@fiware.org"
        exampleLDNormalized = open_json(callNGSILDNormalized)
        exampleLDKeyvalues = open_json(callNGSILDKeyvalues)
        if "@context" in exampleLDKeyvalues:
            exampleV2Keyvalues = exampleLDKeyvalues.copy()
            context = exampleV2Keyvalues.pop("@context")
        exampleV2Normalized = keyvalues2normalized_v2(exampleV2Keyvalues)
        path = "./" + dataModel
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        try:
            os.mkdir(path + "/examples")
        except OSError:
            print("Creation of the examples directory %s failed" % path)
        with open(path + "/examples/example.json", "w") as outputFile:
            json.dump(exampleV2Keyvalues, outputFile, indent=2)
        with open(path + "/examples/example.jsonld", "w") as outputFile:
            json.dump(exampleLDKeyvalues, outputFile, indent=2)
        with open(path + "/examples/example-normalized.json", "w") as outputFile:
            json.dump(exampleV2Normalized, outputFile, indent=2)
        with open(path + "/examples/example-normalized.jsonld", "w") as outputFile:
            json.dump(exampleLDNormalized, outputFile, indent=2)

