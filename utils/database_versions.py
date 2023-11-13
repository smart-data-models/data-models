################################################################################
#
#  Licensed to the FIWARE Foundation (FF) under one
#  or more contributor license agreements. The FF licenses this file
#  to you under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
from github import Github
import time

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


def last_commit_date_link(filePath, repoName, credentialsFile):
    # this functon returns the date of the last modification (commit) on a specific file
    # filePath is the path of the file to be checked. i.e. WeatherForecast/schema.json
    # repo id the repoName in github. i.e. dataModel.Weather

    import json
    import requests

    credentials = open_json(credentialsFile)
    globalUser = credentials["globalUser"]
    token = credentials["token"]

    organization = "smart-data-models"
    gh_session = requests.Session()
    gh_session.auth = (globalUser, token)

    url = "https://api.github.com/repos/" + organization + "/" + repoName + "/commits?path=" + filePath + "&page=1&per_page=1"
    print(url)

    payload = json.loads(gh_session.get(url).text)
    print(payload)
    print("----------------")

    return [payload[0]["commit"]["committer"]["date"], payload[0]["commit"]["url"]]


def check_version(subject, datamodel, version, linktoversion, date, other):
    # it assumes that there is a local host database with the versions in a collection called versions
    # if datamodel or subject is empty, then return False
    # if linktoversion is not "" and there is not such version then insert this version and return True
    # if linktoversion is not "" and there is such version then returns the link to the current version
    # if linktoversion is "" then returns the versions of this data model if it is not empty
    # if data model is not empty but version is empty it returns all the versions
    # other is a dict containing additional info to store with the version
    from pymongo import MongoClient
    server = ""
    dbName = "smartdatamodels"
    collection = "versions"


    if datamodel == "" or subject == "":
        return False
    else:
        client = MongoClient('127.0.0.1', 27017)
        db = client[dbName]
        collversions = db[collection]

        if linktoversion == "":  # just a query
            if version == "":
                query = collversions.find({"dataModel": datamodel})
            else:
                query = collversions.find({"dataModel": datamodel, "version": version})
            if len(query) == 0:
                return False
            else:
                output = []
                for result in query:
                    output.append(result)
                return output
        else:  # it is trying to update a version
            maxversion = ""
            query = collversions.find({"dataModel": datamodel})
            for result in query:
                currentversion = result["version"]
                if currentversion > maxversion:
                    maxversion = currentversion
            if maxversion > version:  # trying to update an old one
                return False
            elif maxversion == version:
                return False
            else:
                payload = {"subject": subject, "dataModel": datamodel, "version": version, "link": linktoversion, "date": date}
                payload.update(other)
                collversions.insert_one(payload)
                return True


credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
# credentials = "/home/fiware/credentials.json
credentials = open_json(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
g = Github(token)


# load list of data models
dataModelsListUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
dataModelsList = open_json(dataModelsListUrl)["officialList"]

limit = 2200
counter = 0
for repo in dataModelsList:
    if counter > limit:
        break
    subject = repo["repoName"]
    datamodels = repo["dataModels"]
    repo = g.get_organization(globalUser).get_repo(subject)
    for datamodel in datamodels:
        print(datamodel)
        counter += 1
        if counter % 20 == 0:
            print("sleeping 10 secs")
            time.sleep(5)
        schemaUrl = "https://raw.githubusercontent.com/smart-data-models/" + subject + "/master/" + datamodel + "/schema.json"
        schema = open_json(schemaUrl)
        schemaVersion = schema["$schemaVersion"]
        filePath = datamodel + "/schema.json"
        repoName = subject
        lastcommit = last_commit_date_link(filePath, repoName, credentialsFile)
        print(lastcommit)
        insert = {"subject": subject, "dataModel": datamodel, "date": lastcommit[0], "version": schemaVersion, "link": lastcommit[1]}
        version = schemaVersion
        linktoversion = schemaUrl
        date = lastcommit[0]
        linktoversion = lastcommit[1]
        other = {"publicLink": linktoversion.replace("api.github.com/repos", "github.com").replace("git/commits", "commit")}
        check_version(subject, datamodel, version, linktoversion, date, other)
