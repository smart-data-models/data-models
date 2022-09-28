################################################################################
#  Licensed to the FIWARE Foundation (FF) under one or more contributor license
#  agreements. The FF licenses this file #  to you under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
################################################################################

# This file takes several @contexts and merge them creating two files
# context.jsonld with the elements successfully merged
# and conflicts.json that shows those attributes clashing.
# clashing in conflicts file has to be solved manually
# INPUT PARAMETERS (merge_subjects_context.json, outputToFile)
# parameter merge_subjects_context.json
# it is the full path to a file where the path to the @contexts will be located
# See an example of the file below
# If not provided it merges all subjects in smart data models program
# {
#   "dataModel.Weather": "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/context.jsonld",
#   "dataModel.Battery": "https://raw.githubusercontent.com/smart-data-models/dataModel.Battery/master/context.jsonld",
#   "dataModel.Building": "https://raw.githubusercontent.com/smart-data-models/dataModel.Building/master/context.jsonld",
#   "dataModel.Device": "https://raw.githubusercontent.com/smart-data-models/dataModel.Device/master/context.jsonld",
# }
# parameter ouputToFile
# when True it outputs tow files conflicts.json and context.jsonld
# conflicts.json stores the conflict in the name of attributes (to be solved manually)
# context.jsonld has the attribute name and the Smart Data Models local IRI


import json
import sys


def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")


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


outputFileConflicts = "conflicts.json"
outputFileContext = "context.jsonld"


# print(sys.argv)
if len(sys.argv) > 1:
    configFile = sys.argv[1]
else:
    configFile = "https://raw.githubusercontent.com/smart-data-models/data-models/master/context/merge_subjects_config.json"
if len(sys.argv) > 2:
    if sys.argv[2] == "True":
        outputToFile = True
    else:
        outputToFile = False
else:
    outputToFile = False  # this variable to True means that the result (context and conflicts will be output as files) otherwise just print them. Default False.
# print(type(outputToFile))
# print(outputToFile)
subjectsDict = open_json(configFile)
if subjectsDict is None:
    print("{\"error\": \"wrong URL\"}")
    sys.exit()
mergedContext = {}
conflicts = {}

for subject in subjectsDict:
    contextUrl = subjectsDict[subject]
    contextDict = open_json(contextUrl)
    if contextDict is None:
        # we have not found this subject context
        continue
    else:
        for element in contextDict["@context"]:
            if element in conflicts:
                # print("element " + element + " is conflicts so we add ")
                conflicts[element].append(contextDict["@context"][element])
            else:
                if element in mergedContext:
                    if mergedContext[element] == contextDict["@context"][element]:
                        # print("element " + element + " is in context but with the same IRI")
                        nada = 0
                    else:
                        conflicts[element] = [contextDict["@context"][element], mergedContext[element]]
                        del mergedContext[element]
                        # print("element " + element + " is repeated with different IRI so added to conflicts ")
                else:
                    # print("element " + element + " is added to the context")
                    mergedContext[element] = contextDict["@context"][element]

output = {"@context": mergedContext, "conflicts": conflicts}
print(json.dumps(output))
# echo("conflicts", conflicts)
# echo("mergedContext", mergedContext)
if outputToFile:
    print("detected outputToFile to True")
    with open(outputFileContext, "w") as file:
        file.write(json.dumps({"@context": mergedContext}, indent=4, sort_keys=True))
    with open(outputFileConflicts, "w") as file:
        file.write(json.dumps(conflicts, indent=4, sort_keys=True))





