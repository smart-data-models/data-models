################################################################################
#  Licensed to the FIWARE Foundation (FF) under one
#  or more contributor license agreements. The FF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# This file creates a drafted json schema according to Smart data models principia
# grab the data from a google sheet (public) and updates a web page based on Wordpress, used in smartdatamodels.org
# some static parameters have to be set prior to execution


import gspread
import json
from wordpress_xmlrpc import Client, WordPressPage
from wordpress_xmlrpc.methods import posts
import datetime
import pytz

def open_json(fileUrl):
    # loads a json file or url and returns it in a dict
    import json
    import requests
    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return json.loads(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return json.loads(file.read())

def post_page(wpUrl, wpUserName, wpPassword, articleTitle, articleContent, pageId):
    # This function updates/creates a page in a wordpress site
    client = Client(wpUrl, wpUserName, wpPassword)
    # Page
    page = WordPressPage()
    page.title = articleTitle
    page.content = articleContent
    # page.terms_names = {'post_tag': articleTags, 'category': articleCategories}
    page.post_status = 'publish'
    # post.thumbnail = attachment_id
    client.call(posts.EditPost(int(pageId), page))
    return pageId


#########################################################
# Static parameters for data model generation           #
#########################################################
#                                                       #

credentialsFile = "/home/fiware/credentials.json"  # Credentials of the WP site, local from the server where the script is executed
# {"smartdatamodelsUser": "user of the WP site"}
# {"smartdatamodelsPass": "pass of the WP site"}
# it has to be right to edit a web page

credentials = open_json(credentialsFile)
SITE_USER = credentials["smartdatamodelsUser"]
SITE_PASS = credentials["smartdatamodelsPass"]
print(SITE_USER)
# url of the spreadsheet (/)It has to be made public). You need a user authorized in sheets API.
# a starting point here https://developers.google.com/sheets/api/guides/authorizing
publicSheetUrl = "https://docs.google.com/spreadsheets/d/1TwXCBI-oedpf9RYpYlLNZnz5Pxl6o6kxHXKINRdJi5c/edit?usp=sharing"

# tab in the spreadsheet containing  the data
workSheet = "dataModel"

# zone of the spreadsheet for recovering the main parameters of the data model
# it is recommended that the rest of the cells are protected
mainParametersRange = "B2:B5"
# zone of the spreadsheet for recovering the data of the properties
mainDataRange = "A9:F80"

# template of schema header for the json schema
schemaHeaderBase = """
{
  "$schema": "http://json-schema.org/schema#",
  "$schemaVersion": "0.0",
  "$id": "https://smart-data-models.github.io/XXsubjectXX/XXdatamodelXX/schema.json",
  "title": " Smart Data Models - XXtitleXX",
  "description": "XXglobaldescriptionXX.",
  "type": "object",
  "allOf": [
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/GSMA-Commons"
    },
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/Location-Commons"
    }
    ]
    }"""

pageInSmartDataModelsSite = 1329  # id of the page where the schema is written

# url of the xml-rpc of the wordpress site
# you need to install the iframe plugin
wpUrl = "https://smartdatamodels.org/xmlrpc.php"
pageContentsBase = """Fill the spreadsheet and click this link, you'll get a drafted json schema documented according to the Smart data models below.
This is an alpha version. Currently there is no option for including array items or object properties. They have to be manually added to these data types.
<h3>Fill the blue cells</h3>
<form action="https://smartdatamodels.org/extra/generator_schema_from_sheet.php">

[iframe src="https://docs.google.com/spreadsheets/d/1TwXCBI-oedpf9RYpYlLNZnz5Pxl6o6kxHXKINRdJi5c/edit#gid=0" width="100%" height="700"]
    <input type="submit" value="Generate Schema" />
</form>
After clicking the button the page will refresh and you have to copy the generated schema below the spreadheet
<a href="https://smartdatamodels.org/extra/generator_schema_from_sheet.php">Link</a>
<h3>SCHEMA</h3>
"""

#

#                                                       #
#########################################################


#########################################################
# gather the main parameters of the data model          #
#########################################################
#                                                       #

# create the object for accessing the spreadsheet
# you've got this when authorizing the sheets API
# path to API credentials of the sheets API
pathToAPICredentials = "/home/fiware/service_account.json"
gc = gspread.service_account(pathToAPICredentials)

# create the worksheet object
wks = gc.open_by_url(publicSheetUrl).worksheet(workSheet)
# retrieve data
mainParameters = wks.get(mainParametersRange)

# assign data to variables (According to the ranges defined previously
subject = mainParameters[0][0]
dataModel = mainParameters[1][0]
title = mainParameters[2][0]
generalDescription = mainParameters[3][0]

# adapt the schema header
schemaHeader = schemaHeaderBase.replace("XXsubjectXX", subject).replace("XXdatamodelXX", dataModel).replace("XXtitleXX", title).replace("XXglobaldescriptionXX", generalDescription)
schema = json.loads(schemaHeader)

#                                                       #
#########################################################

#########################################################
# gather the main schema properties  of the data model  #
#########################################################
#                                                       #
mainData = wks.get(mainDataRange)

# initialize variables to create the schema
propertiesNames = []
NGSIType = []
dataType = []
other = []
propertyDescriptions = []

# fill the variables with the contents of the spreadsheet to generate schema
for element in mainData:
    try:
        if len(element[0])== 0:
            break
        propertiesNames.append(element[0])
        print(element[0])
    except:
        break
    try:
        NGSIType.append(element[1])
    except:
        continue
    try:
        dataType.append(element[2])
    except:
        dataType.append("")
    try:
        other.append(element[3])
    except:
        other.append("")
    try:
        propertyDescriptions.append(element[4])
    except:
        propertyDescriptions.append("")

#                                                       #
#########################################################

#########################################################
# gather the main schema properties  of the data model  #
#########################################################
#                                                       #

properties = {}

for index in range(len(propertiesNames)):
    print(index)
    if NGSIType[index] == "Geoproperty":
        payload = {"$ref": "http://geojson.org/schema/Geometry.json"}
    elif NGSIType[index] == "Relationship":
        payload = {"type": "string", "format": "uri", "description": "Relationship. Model:'https://schema.org/URL'. " + propertyDescriptions[index]}
    elif NGSIType[index] == "Property":
        itemPayload = {}
        if dataType[index] == "string":
            if len(other[index]) > 0:
                itemPayload["type"] = "string"
                itemPayload["description"] = "Property. Model:'https://schema.org/Text'. " + propertyDescriptions[index]
                print(other[index])
                rawOther = json.loads(other[index])
                print(type(rawOther))
                for element in rawOther:
                    itemPayload[element] = rawOther[element]
                payload = itemPayload
            else:
                payload = {"type": "string", "description": "Property. Model:'https://schema.org/Text'. " + propertyDescriptions[index]}
        elif dataType[index] == "number":
            if len(other[index]) > 0:
                itemPayload["type"] = "number"
                itemPayload["description"] = "Property. Model:'https://schema.org/Number'. " + propertyDescriptions[index]
                print(other[index])
                rawOther = json.loads(other[index])
                print(type(rawOther))
                for element in rawOther:
                    itemPayload[element] = rawOther[element]
                payload = itemPayload
            else:
                payload = {"type": "number", "description": "Property. Model:'https://schema.org/Number'. " + propertyDescriptions[index]}
        elif dataType[index] == "uri":
            payload = {"type": "string", "format": "uri", "description": "Property. Model:'https://schema.org/URL'. " + propertyDescriptions[index]}
        elif dataType[index] == "date-time":
            payload = {"type": "string", "format": "date-time", "description": "Property. Model:'https://schema.org/DateTime'. " + propertyDescriptions[index]}
        elif dataType[index] == "boolean":
            payload = {"type": "boolean", "description": "Property. Model:'https://schema.org/Boolean'. " + propertyDescriptions[index]}
        elif dataType[index] == "array":
            payload = {"type": "array", "description": "Property. " + propertyDescriptions[index], "items": {}}
        elif dataType[index] == "object":
            payload = {"type": "object", "description": "Property. " + propertyDescriptions[index], "properties": {}}
        else:
            payload = {}
    else:
        payload = {}
    properties[propertiesNames[index]] = {}
    properties[propertiesNames[index]] = payload
schema["allOf"].append({"properties": properties})

#                                                       #
#########################################################

#########################################################
# update the wordpress page with the json schema        #
#########################################################
#                                                       #

wpUserName = SITE_USER
wpPassword = SITE_PASS
tz = pytz.timezone("Europe/Madrid")
timestamp = str(datetime.datetime.now(tz=tz))
articleTitle = "Draft a data model"
articleContent = pageContentsBase
articleContent += "<br><br>"
articleContent += "draft schema generated at " + str(timestamp) + "<br>"
articleContent += "<pre>" + json.dumps(schema, indent=4) +"</pre>"

post_page(wpUrl, wpUserName, wpPassword, articleTitle, articleContent, pageInSmartDataModelsSite)

# logging execution just in case to test the script is running
with open("output.txt", "a") as file:
    file.write(json.dumps(schema))
print(schema)