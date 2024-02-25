# input the term
# output the page created or updated
# source of truth repository the mongodatabase
from pymongo import MongoClient
import os
import requests
import json
import yaml

# database where the attributes are stored
dbName = "smartdatamodels"
collectionName = "properties"

# connection with the database
client = MongoClient()
db = client[dbName]
colProperties = db[collectionName]

# root of the files
root = "/var/www/html/"

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


def open_yaml(fileUrl):
    # import yaml
    from ruamel.yaml import YAML
    yaml_object = YAML(typ='safe', pure=True)
    import requests
    try:
        if fileUrl[0:4] == "http":
            # es URL
            pointer = requests.get(fileUrl)
            return yaml_object.load(pointer.content.decode('utf-8'))
    except:
        return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return yaml_object.load(file.read())
        except:
            return None


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


def create_context_entity_page(entity, subject):
    # This function assumes the location of the mongodb with the terms
    # in localhost and the collection has to be 'properties' into the database 'smartdatamodels'
    root = "/var/www/html/"
    ### retrieve the data
    queryTerm = {"dataModel": entity, "repoName": subject}
    query = colProperties.find(queryTerm)
    queryResult = [entity_ for entity_ in query]
    echo("query result", queryResult)
    echo("type of query result", type(queryResult))
    # echo("type of query result 0", type(queryResult[0]))
    # dataModelsUsed = []
    # dataTypesUsed = []
    # propertiesDescriptions = []
    attributesList = []
    yamlUrl = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + entity + "/model.yaml"
    entityDict = open_yaml(yamlUrl)
    print(entityDict)
    for entity_ in queryResult:
        if "parentId" in entity_:
            continue
        elif "subpropertiesContext" in entity_:
            attributesList.append((entity_["property"], entity_["context"], entity_["subpropertiesContext"]))
        else:
            attributesList.append((entity_["property"], entity_["context"], ""))
    definition = entityDict[entity]["description"]
    version = entityDict[entity]["x-version"]
    schemaUrl = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + entity + "/schema.json"
    examplesUrl = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + entity + "/examples"
    adoptersUrl= "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + entity + "/ADOPTERS.yaml"
    contributorsUrl = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + "CONTRIBUTORS.yaml"
    requiredAttributes = entityDict[entity]["required"]


    #########################
    ### CREATING THE PAGE ###
    #########################
    #initialize the styles
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
    html += "<div class=\"divTable blueTable\"><div class=\"divTableHeading\"><div class=\"divTableRow\"><div class=\"divTableHead\"><h1>" + entity + "</h1></div></div></div>"

    ### Definition of the entity
    html += rowDivStart + "<h2>" + "Definition" + "</h2>" + definition + rowDivEnd

    ### Version of the entity
    html += rowDivStart + "<h2>" + "Version" + "</h2>" + version + rowDivEnd

    ### Schema of the entity
    html += rowDivStart + "<h2>" + "Original Schema" + "</h2>" + "<a href=\"" + schemaUrl + "\">" + schemaUrl + "</a>" + rowDivEnd

    ### Contributors of the entity
    html += rowDivStart + "<h2>" + "Contributors of the Subject" + "</h2>" + "<a href=\"" + contributorsUrl + "\">" + contributorsUrl + "</a>" + rowDivEnd

    ### ADOPTERS of the entity
    html += rowDivStart + "<h2>" + "Adopters of the data model" + "</h2>" + "<a href=\"" + adoptersUrl + "\">" + adoptersUrl + "</a>" + rowDivEnd

    ### Examples of the entity
    html += rowDivStart + "<h2>" + "Examples of the data model" + "</h2>" + "<a href=\"" + examplesUrl + "\">" + examplesUrl + "</a>" + rowDivEnd

    ### attributes List
    html += rowDivStart + "<h3>" + "Attributes of the entity" + "</h3> " + rowDivEnd
    html += "<ul>"
    for attribute, context, subcontext in attributesList:
        if "@" in context:
            html += "<li>" + attribute + "</li>"
        else:
            html += "<li>" + "<a href=" + chr(34) + context + \
                    chr(34) + ">" + attribute + "</a></li>"
        if isinstance(subcontext, list):
            html += "<ul>"
            for subprop in subcontext:
                for k, v in subprop.items():
                    if "@" in v:
                        html += "<li>" + k + "</li>"
                    else:
                        html += "<li>" + "<a href=" + chr(34) + v + \
                        chr(34) + ">" + str(k) + "</a></li>"
            html += "</ul>"
    html += "</ul>"

 ### Required attributes List
    html += rowDivStart + "<h3>" + "Required attributes" + "</h3> " + rowDivEnd
    html += "<ul>"
    for attribute in requiredAttributes:
        html += "<li>" + attribute + "</li>"
    html += "</ul>"


    path = root + subject
    htmlFile = path + "/" + entity
    print("The html file is " + htmlFile)
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    with open(htmlFile, "w+") as file:
        file.write(html)


configFile ="datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)

repoName = dataModelsToPublish["subject"]
subject = repoName
dataModels = dataModelsToPublish["dataModels"]
if isinstance(dataModels, str):
    dataModels = [dataModels]
# creating the pages here for the data models
indexPage = "sitemap.txt"
sitemapUrl = "https://smartdatamodels.org/sitemap.txt"
pointer = requests.get(sitemapUrl).text
cr = chr(10)
uris = pointer.split(cr)

print(dataModels)
newEntitiesUris = []
for dataModel in dataModels:
    create_context_entity_page(dataModel, repoName)
    newEntitiesUris.append("https://smartdatamodels.org/" + subject + "/" + dataModel)

for newEntityUri in newEntitiesUris:
    if newEntityUri not in uris:
        uris.append(newEntityUri)


indexContent = cr.join(uris)

with open(root + "sitemap.txt", "w+") as file:
    file.write(indexContent)
