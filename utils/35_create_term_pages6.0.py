# input the term
# output the page created or updated
# source of truth repository the mongodatabase
# TEMPLATE DE LA PÁGINA done
# TITLE: name of the term: done
# DATA TYPE
# DEFINITION/S. doubt
# list of the data models (link) (IN REPO) link where the term is used  + data of the ADOPTERS.YAML
import yaml
from datetime import datetime
from pymongo import MongoClient
from operator import itemgetter
import os

# database where the attributes are stored
dbName = "smartdatamodels"
collectionName = "properties"

# connection with the database
client = MongoClient()
db = client[dbName]
colProperties = db[collectionName]

# root of the files
root = "/var/www/html/"


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


def open_jsonref(fileUrl):
    import jsonref
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return jsonref.loads(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return jsonref.loads(file.read())


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def create_context_page(term):
    # This function assumes the location of the mongodb with the terms
    # in localhost and the collection has to be 'properties' into the database 'smartdatamodels'

    ### retrieve the data
    exceptions = ["id"]
    queryTerm = {"property": term}
    query = colProperties.find(queryTerm)
    queryResult = [property_ for property_ in query]
    echo("query result", queryResult)
    echo("type of query result", type(queryResult))
    # echo("type of query result 0", type(queryResult[0]))
    dataModelsUsed = set()
    dataTypesUsed = set()
    propertiesDescriptions = set()
    modelDescriptions = set()
    unitsDescriptions = set()
    dataTypesNGSIUsed = set()
    subpropertiesContext = []
    parentContext = set()
    for prop in queryResult:
        if prop["property"] in exceptions:
            break
        if "dataModel" in prop:
            dataModelsUsed.add((prop["dataModel"], prop["repoName"]))
        if "description" in prop:
            propertiesDescriptions.add(prop["description"])
        if "type" in prop:
            dataTypesUsed.add(prop["type"])
        if "model" in prop:
            modelDescriptions.add(prop["model"])
        if "units" in prop:
            unitsDescriptions.add(prop["units"])
        if "typeNGSI" in prop:
            dataTypesNGSIUsed.add(prop["typeNGSI"])
        if "parentContext" in prop:
            parentContext.add(prop["parentContext"])
        if "subpropertiesContext" in prop:
            subpropertiesContext.append(prop["subpropertiesContext"])

    rootSmartDataModels = "https://github.com/smart-data-models/"

    #########################
    ### CREATING THE PAGE ###
    #########################
    # initialize the styles
    html = """<style>
div.blueTable {
  border: 1px solid #1C6EA4;
  background-color: #EEEEEE;
  width: 100%;
  text-align: left;
  border-collapse: collapse;
}
.divTable.blueTable .divTableCell, .divTable.blueTable .divTableHead {
  border: 1px solid #AAAAAA;
  padding: 3px 2px;
}
.divTable.blueTable .divTableBody .divTableCell {
  font-size: 13px;
}
.divTable.blueTable .divTableRow:nth-child(even) {
  background: #D0E4F5;
}
.divTable.blueTable .divTableHeading {
  background: #1C6EA4;
  background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);
  border-bottom: 2px solid #444444;
}
.divTable.blueTable .divTableHeading .divTableHead {
  font-size: 15px;
  font-weight: bold;
  color: #FFFFFF;
  border-left: 2px solid #D0E4F5;
}
.divTable.blueTable .divTableHeading .divTableHead:first-child {
  border-left: none;
}

.blueTable .tableFootStyle {
  font-size: 14px;
  font-weight: bold;
  color: #FFFFFF;
  background: #D0E4F5;
  background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);
  border-top: 2px solid #444444;
}
.blueTable .tableFootStyle {
  font-size: 14px;
}
.blueTable .tableFootStyle .links {
         text-align: right;
}
.blueTable .tableFootStyle .links a{
  display: inline-block;
  background: #1C6EA4;
  color: #FFFFFF;
  padding: 2px 8px;
  border-radius: 5px;
}
.blueTable.outerTableFooter {
  border-top: none;
}
.blueTable.outerTableFooter .tableFootStyle {
  padding: 3px 5px;
}
/* DivTable.com */
.divTable{ display: table; }
.divTableRow { display: table-row; }
.divTableHeading { display: table-header-group;}
.divTableCell, .divTableHead { display: table-cell;}
.divTableHeading { display: table-header-group;}
.divTableFoot { display: table-footer-group;}
.divTableBody { display: table-row-group;}
</style>
    """
    page = {}

    ### Heading
    rowDivStart = "<div class=\"divTableRow\"><div class=\"divTableCell\">"
    rowDivEnd = "</div></div>"
    html += "<div class=\"divTable blueTable\"><div class=\"divTableHeading\"><div class=\"divTableRow\"><div class=\"divTableHead\"><h1>" + term + "</h1></div></div></div>"
    page["property"] = term

    ### Definition of the term
    if len(propertiesDescriptions) > 1:
        msg = "There are alternatives descriptions in other data models, please check it below if it fits you needs"
        propertiesDescriptions = list(propertiesDescriptions)
        html += rowDivStart + "<h2>" + "Definition" + "</h2>" + str(
            propertiesDescriptions[0]) + "<br>" + msg + "<br>" + rowDivEnd
        page["description"] = propertiesDescriptions[0]
    elif len(propertiesDescriptions) == 1:
        propertiesDescriptions = list(propertiesDescriptions)
        html += rowDivStart + "<h2>" + "Definition" + "</h2>" + str(propertiesDescriptions[0]) + "<br>" + rowDivEnd
        page["description"] = propertiesDescriptions[0]
    else:
        msg = "The information is pending, find more details in the schema"
        html += rowDivStart + "<h2>" + "Definition" + "</h2>" + msg + rowDivEnd
        page["description"] = msg

    ### Data type of the term
    if len(dataTypesUsed) > 1:
        msg = "There are alternatives descriptions in other data models, please check it below if it fits you needs"
        # dataTypesUsed = max(set(dataTypesUsed), key = dataTypesUsed.count)
        dataTypesUsed = list(dataTypesUsed)
        html += rowDivStart + "<h3>" + "Data Types" + "</h3> " + str(
            dataTypesUsed[0]) + "<br>" + msg + "<br>" + rowDivEnd
        page["type"] = dataTypesUsed[0]
    elif len(dataTypesUsed) == 1:
        dataTypesUsed = list(dataTypesUsed)
        html += rowDivStart + "<h3>" + "Data Types" + "</h3> " + str(dataTypesUsed[0]) + "<br>" + rowDivEnd
        page["type"] = dataTypesUsed[0]
    else:
        msg = "The specific type could have several types or different formats/patterns, find more details in the schema"
        html += rowDivStart + "<h3>" + "Data Types" + "</h3> " + msg + rowDivEnd
        page["type"] = msg

    ### Parent of the property
    if len(parentContext):
        htmlParent, pageParent = "", ""
        for parent_ in parentContext:
            if "@" in parent_:
                htmlParent += parent_.split("/")[-1] + "<br>"
                pageParent += parent_.split("/")[-1]
            else:
                htmlParent += \
                    "<a href=" + chr(34) + parent_ + \
                    chr(34) + ">" + parent_.split("/")[-1] + "</a><br>"

                pageParent += \
                    "[" + parent_.split("/")[-1] + "](" + parent_ + \
                    ")"
        html += rowDivStart + "<h3>" + "Parent Property" + "</h3>" + htmlParent + rowDivEnd
        page["parentContext"] = pageParent

    ### subpropertiesContext of the property
    if len(subpropertiesContext):
        subpropertiesContext = subpropertiesContext[0]
        htmlSub, pageSub = "", ""
        for subprop_ in subpropertiesContext:
            for k, v in subprop_.items():
                if "@" in v:
                    htmlSub += str(k) + "<br>"
                    pageSub += str(k)
                else:
                    htmlSub += \
                        "<a href=" + chr(34) + v + \
                        chr(34) + ">" + str(k) + "</a><br>"
                    pageSub += \
                        "[" + str(k) + "](" + v + \
                        ")"
        html += rowDivStart + "<h3>" + "Sub-properties" + "</h3> " + htmlSub + rowDivEnd
        page["subpropertiesContext"] = pageSub

    ### List the data models which use the term
    html += rowDivStart + "<h3>" + "List of data models using the term in this subject" + "</h3>"

    dataModelsString = ""
    page["dataModelsUsingProperty"] = {}
    for dm, subject in sorted(dataModelsUsed, key=lambda x: x[1]):
        dataModelsString += "<a href=" + chr(34) + rootSmartDataModels + subject + "/tree/master/" + dm + chr(
            34) + ">" + dm + "</a><br>"
        page["dataModelsUsingProperty"][
            dm] = "[" + rootSmartDataModels + subject + "/tree/master/" + dm + "](" + dm + ")"
    html += dataModelsString + rowDivEnd

    ### NGSI type of the term in this subject
    if len(dataTypesNGSIUsed) > 0:
        dataTypesNGSIUsed = list(dataTypesNGSIUsed)
        html += rowDivStart + "<h3>" + "NGSI type of the term in this subject" + "</h3> " + "<br>".join(
            dataTypesNGSIUsed) + rowDivEnd
        page["typeNGSI"] = dataTypesNGSIUsed
    else:
        msg = "The specific type could have several types or different formats/patterns, find more details in the schema"
        html += rowDivStart + "<h3>" + "NGSI type of the term in this subject" + "</h3> " + msg + rowDivEnd
        page["typeNGSI"] = msg

    ### the model of the term in this subject
    if len(modelDescriptions) > 0:
        modelDescriptions = list(modelDescriptions)
        html += rowDivStart + "<h3>" + "Models of the term in this subject" + "</h3> " + "<br>".join(
            modelDescriptions) + rowDivEnd
        page["model"] = modelDescriptions

    ### the units of the term in this subject
    if len(unitsDescriptions) > 0:
        unitsDescriptions = list(unitsDescriptions)
        html += rowDivStart + "<h3>" + "Units of the term in this subject" + "</h3> " + "<br>".join(
            unitsDescriptions) + rowDivEnd
        page["units"] = unitsDescriptions

    return [html, page]


configFile = "datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)
repoName = dataModelsToPublish["subject"]
dataModels = dataModelsToPublish["dataModels"]

coreContextDictUrl = "etsi_core_context.json"
etsiContext = open_json(coreContextDictUrl)['@context']

commonContextUrl = f"https://github.com/smart-data-models/data-models/raw/master/context/common-context.jsonld"
commonContext = open_json(commonContextUrl)["@context"]

commonContextExp = list(commonContext.keys())
etsiContextExp = list(etsiContext.keys())

if isinstance(dataModels, str):
    dataModels = [dataModels]
print(dataModels)
for dataModel in dataModels:
    globalQuery = db.properties.find({"repoName": repoName, "dataModel": dataModel})
    # print(globalQuery)
    globalResult = [property_ for property_ in globalQuery]

    exceptions = ["id"]
    indexPage = "sitemap.txt"
    indexContent = ""

    rootUrl = "https://smartdatamodels.org"
    for register in globalResult:
        if "property" in register:
            if (register["property"] in exceptions) or (register["property"] in etsiContextExp):
                continue
            elif register["property"] in commonContextExp:  # if the property is in the common-schema.json
                term = register["property"]
                subject = ""
                htmlFile = root + term
                yamlFile = root + term + ".yaml"
                indexContent += rootUrl + "/" + term + chr(10)
                indexContent += rootUrl + "/" + term + ".yaml" + chr(10)
                output = create_context_page(term)
                htmlPage = output[0]
                yamlPage = output[1]
                path = root + subject
                # Check whether the specified path exists or not
                isExist = os.path.exists(path)
                if not isExist:
                    # Create a new directory because it does not exist
                    os.makedirs(path)
                    print("The new directory is created!")
                with open(htmlFile, "w+") as file:
                    file.write(htmlPage)

                with open(yamlFile, "w+") as file:
                    yaml.dump(yamlPage, file, allow_unicode=True, default_flow_style=False)
            else:
                subject = repoName
                term = register["property"]
                echo("this is the term", term)
                echo("this is the type of the term", type(term))
                htmlFile = root + subject + "/" + term
                yamlFile = root + subject + "/" + term + ".yaml"
                indexContent += rootUrl + "/" + subject + "/" + term + chr(10)
                indexContent += rootUrl + "/" + subject + "/" + term + ".yaml" + chr(10)
                output = create_context_page(term)
                htmlPage = output[0]
                yamlPage = output[1]
                path = root + subject
                # Check whether the specified path exists or not
                isExist = os.path.exists(path)
                if not isExist:
                    # Create a new directory because it does not exist
                    os.makedirs(path)
                    print("The new directory is created!")
                with open(htmlFile, "w+") as file:
                    file.write(htmlPage)

                with open(yamlFile, "w+") as file:
                    yaml.dump(yamlPage, file, allow_unicode=True, default_flow_style=False)

with open(root + indexPage, "a") as file:
    file.write(indexContent)
