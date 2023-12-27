# Check whether the properties are existent in the database already

# TODO: import the function from python package by "from pysmartdatamodel.utils import *"

from pymongo import MongoClient

def is_property_already_existed(output, yamlDict):
    try:
        mongoDb = "smartdatamodels"
        mongoCollection = "properties"
        client = MongoClient()
        db = client[mongoDb]
        collProperties = db[mongoCollection]
        commonProperties =["id", "name", "description", "location", "seeAlso", "dateCreated", "dateModified", "source", "alternateName", "dataProvider", "owner", "address", "areaServed", "type"]
        existing = "alreadyUsedProperties"
        available = "availableProperties"

        #print("llego a la funcion")
        output[existing] = []
        output[available] = []

        for key in yamlDict:
            if key in commonProperties:
                continue
            #print(key)
            lowKey = key.lower()
            patternKey = "^"+ lowKey + "$"
            queryKey = {"property": {"$regex": patternKey, "$options": "i"}}

            results = list(collProperties.find(queryKey))
            #print(len(results))
            if len(results) > 0:
                definitions= []
                dataModelsList = []
                types = []
                for index, item in enumerate(results):
                    dataModelsList.append(str(index + 1) + ".-" + item["dataModel"])
                    #print(item["type"])
                    if "description" in item or "type" in item:
                        if "description" in item:
                            definitions.append(str(index + 1) + ".-" + item["description"])
                        else:
                            definitions.append(str(index + 1) + ".- missing description")
                        if "type" in item:
                            types.append(str(index + 1) + ".-" +  item["type"])
                        else:
                            types.append(str(index + 1) + ".- missing type")
                    else:
                        output[existing].append({"Error": lowKey})
                output[existing].append({key: "Already used in data models: " + ",".join(dataModelsList) + " with these definitions: " + chr(13).join(definitions) + " and these data types: " + ",".join(types)})
            else:
                output[available].append({key: "Available"})

    except:
        output[existing].append({"Error": lowKey})
    
    return output

