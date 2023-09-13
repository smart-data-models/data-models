from github import Github
import os
import errno
import requests
        
def exist_page(url):
    # check if a web page exists
    # returns [true , web content] if successes
    # otherwise returns [false, error] if it fails
    import requests
    output = []
    try:
        pointer = requests.get(url)
        if pointer.status_code == 200:
            return [True, pointer.text]
        else:
            return [False, pointer.status_code]
    except:
        return [False, "wrong domain"]


def translation(sentence, sourceLang, targetLang, authKey):
    # sentence is the text to be translated
    # sourcelang is the language source of the text in sentence
    # targetlang is the target language for the text sentence
    import requests
    import json
    import urllib.parse

    supportedTargetLanguages = ["DE", "EN-GB", "EN-US", "ES", "FR", "IT", "JA", "NL", "PL", "PT-PT", "PT-BR", "RU",
                                "ZH"]
    encodings = {}
    # encodings["DE"] = "cp1252"
    encodings["DE"] = "utf-8"
    encodings["EN-GB"] = "cp1252"
    encodings["EN-US"] = "cp1252"
    encodings["ES"] = "latin-1"
    encodings["FR"] = "cp1252"
    encodings["IT"] = "utf-8"
    encodings["JA"] = "utf-8"
    encodings["NL"] = "cp1252"
    encodings["PL"] = "cp1252"
    encodings["PT-PT"] = "cp1252"
    encodings["PT-BR"] = "cp1252"
    encodings["RU"] = "cp1252"
    encodings["ZH"] = "utf-8"
    matches = {}
    matches["ES"] = ["á", "é", "í", "ó", "ú", "ñ", "ü", "Á", "É", "Í", "Ó", "Ú"]
    matches["FR"] = ["á", "é", "í", "ó", "ú", "à", "è", "ù", "â", "ê", "î", "ô", "û", "ë", "ï", "ÿ", "ç", "Á", "É", "Í", "Ó", "Ú"]
    matches["DE"] = []
    #matches["IT"] = ["é", "è"]
    matches["IT"] = []
    matches["JA"] = []
    matches["ZH"] = []
    # cambio manual para cuando hay que hacerlo de verdad
    actualTranslation = True

    if actualTranslation:
        if targetLang not in supportedTargetLanguages:
            return ("language not supported")
        elif targetLang == "EN-US" and sourceLang == "EN":
            return sentence
        elif targetLang == "EN-GB" and sourceLang == "EN":
            return sentence
        else:
            payload = {
                "Host": "api.deepl.com",
                "Accept": "*/*",
                "User-Agent": "Fiware Smart data models",
                "Content-Type": "application/x-www-form-urlencoded;charset=latin-1",
                "Content-Length": len(sentence),
                "Origin": "https://www.mywbsite.fr",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
                "Accept-Charset": "utf-8;q=0.7,*;q=0.3"
            }
            headers = {}
            urlRoot = "https://api.deepl.com/v2/translate?"
            url = urlRoot + "auth_key=" + authKey + "&" + "text=" + urllib.parse.quote(
                sentence) + "&" + "target_lang=" + targetLang + "&" + "source_lang=" + sourceLang
            print(url)

            response = requests.post(url, data=json.dumps(payload), headers=headers)
            answer = response.text
            print(answer)
            print(response.headers)
            translatedDict = dict(response.json())
            output = translatedDict["translations"][0]["text"]
            if any(x in output for x in matches[targetLang]):
                # if is normal
                return output
            else:
                return output.encode(encodings[targetLang]).decode("utf-8")
    else:
        return sentence


def make_title(text):
    output = ""
    output += text + chr(10)
    output += "=" * len(text) + chr(13)
    return output


def make_header(level, text):
    if level < 1 or level > 6:
        return text
    else:
        return chr(13) + "#" * level + " " + text + chr(10)


def make_bold(text):
    return " **" + text + "** "


def make_monospace(text):
    return " `" + text + "` "


def make_monospace_bold(text):
    return " ***" + text + "*** "


def make_literal(option, text):
    return chr(10) + chr(13) + "```" + option + chr(10) + chr(13) + text + chr(10) + "```" + chr(10)


def make_paragraph(text):
    return chr(10) + chr(13) + text + chr(10)


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


def read_yaml(fileUrl):
    import yaml
    from yaml.resolver import Resolver
    import re
    import requests
    # required for avoiding that No was replace by false
    for ch in "OoYyNn":
        if ch in Resolver.yaml_implicit_resolvers:
            if len(Resolver.yaml_implicit_resolvers[ch]) == 1:
                del Resolver.yaml_implicit_resolvers[ch]
            else:
                Resolver.yaml_implicit_resolvers[ch] = [x for x in Resolver.yaml_implicit_resolvers[ch] if x[0] != 'tag:yaml.org,2002:bool']


    if fileUrl[0:4] == "http":
        # es URL
        pointer = requests.get(fileUrl)
        return yaml.safe_load(pointer.content.decode('utf-8'))
    else:
        # es file
        file = open(fileUrl, "r")
        return yaml.safe_load(file.read())


def github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token):
    from github import Github
    g = Github(token)
    repo = g.get_organization(globalUser).get_repo(repoName)
    try:
        file = repo.get_contents("/" + fileTargetPath)
        update = True
    except:
        update = False
    if update:
        commit = repo.update_file(fileTargetPath, message, contentVariable, file.sha)
    else:
        commit = repo.create_file(fileTargetPath, message, contentVariable, "master")
    return commit


def comment_spec(section, opencomment):
    newline = chr(13) + chr(10)
    if opencomment:
        return "<!-- " + section + " -->" + newline
    else:
        return "<!-- /" + section + " -->" + newline



#credentialsFile = "/home/aabella/transparentia/CLIENTES/EU/FIWARE/credentials.json"
credentialsFile = "/home/fiware/credentials.json"
credentials = open_jsonref(credentialsFile)
token = credentials["token"]
globalUser = credentials["globalUser"]
authKey = credentials["deepLKey"]
english = "EN"
alphabeticOrdered = "Sorted alphabetically (click for details)"
examplePayloads = "Example payloads"
requiredPropertiesHeader = "Required properties"
noRequiredProperties = "No required properties"
newLine = chr(10) + chr(13)
unitsWarning = "See [FAQ 10](https://smartdatamodels.org/index.php/faqs/) to get an answer on how to deal with magnitude units"


g = Github(token)
localExecution = False

# static values
modelYaml = "model.yaml"
listOfPropertiesText = "## List of properties"
warningTypes = "<sup><sub>[*] If there is not a type in an attribute is because it could have several types or different formats/patterns</sub></sup>"
techDescriptionOfPropertiesText = "Data Model description of properties"
uselessPRText = "[document generated automatically](https://docs.google.com/presentation/d/e/2PACX-1vTs-Ng5dIAwkg91oTTUdt8ua7woBXhPnwavZ0FxgR8BsAI_Ek3C5q97Nd94HS8KhP-r_quD4H0fgyt3/pub?start=false&loop=false&delayms=3000#slide=id.gb715ace035_0_60)"

licenseMessageStart = "[Open License](https://github.com/smart-data-models//"
licenseMessageEnd = "/LICENSE.md)"


urlNotesRoot = "https://smart-data-models.github.io"

# static definitions
propertyTypes = ["Property", "Relationship", "Geoproperty"]


specFileNameRoot = "spec"

# languages = ["DE", "EN-GB", "EN-US", "ES", "FR", "IT", "JA", "NL", "PL", "PT-PT", "PT-BR", "RU", "ZH"]

configFile ="datamodels_to_publish.json"
dataModelsToPublish = open_jsonref(configFile)


echo("subject", dataModelsToPublish["subject"])
echo("dataModels", dataModelsToPublish["dataModels"])
echo("filter or no ", dataModelsToPublish["filterDataModels"])
echo("languages ", dataModelsToPublish["languages"])

filterRepo = [dataModelsToPublish["subject"]]
filterDataModel = dataModelsToPublish["dataModels"]
allowFilterDataModel = dataModelsToPublish["filterDataModels"]
languages = dataModelsToPublish["languages"]

repoName = dataModelsToPublish["subject"]
echo("repoName", repoName)
dataModels = dataModelsToPublish["dataModels"]
if isinstance(dataModels, str):
    dataModels = [dataModels]

for dataModel in dataModels:
    print("data model = " + dataModel)
    print(not (dataModel in filterDataModel and len(filterDataModel) > 0))
    if dataModel in filterDataModel or not allowFilterDataModel:
        # location of the file
        path = "/" + dataModel + "/doc/"
        # location of the yaml version
        schemaUrl = urlNotesRoot + "/" + repoName + "/" + dataModel + "/" + "schema.json"

        # specification will be composed by several sections
        for lang in languages:
            print("Starting with the language " + lang)
            if lang == english or lang == "EN-US":
                specFileName = specFileNameRoot + ".md"
            else:
                specFileName = specFileNameRoot + "_" + lang + ".md"
            #########################################
            # 1: Header with the name of the entity #
            #########################################
            specContent = comment_spec("10-Header", True)
            specContent += "[![Smart Data Models](https://smartdatamodels.org/wp-content/uploads/2022/01/SmartDataModels_logo.png \"Logo\")](https://smartdatamodels.org)" + chr(10)  + chr(13)

            # this is the name for the final push into github repo
            fullFileName = dataModel + "/doc/" + specFileName
            specContent += make_title(translation("Entity: " + dataModel, english, lang, authKey))
            specContent += comment_spec("10-Header", False)

            ######################################################
            # 1.5: LICENSE AND MODIFICATION WARNING OF THE  SPEC #
            ######################################################

            specContent += comment_spec("15-License", True)
            licenseMessage = licenseMessageStart + repoName + "/blob/master/" + dataModel + licenseMessageEnd
            print(licenseMessage)
            specContent += make_paragraph(translation(licenseMessage, english, lang, authKey))
            specContent += make_paragraph(translation(uselessPRText, english, lang, authKey))
            specContent += comment_spec("15-License", False)

            #########################################
            # 2: Description of the entity          #
            #########################################
            specContent += comment_spec("20-Description", True)
            urlModelFile = urlNotesRoot + "/" + repoName + "/" + dataModel + "/" + modelYaml
            print(urlModelFile)
            request = requests.get(urlModelFile)
            print("status code:" + str(request.status_code))
            if request.status_code == 200:
                print("Reading model")
                model = read_yaml(urlModelFile)
                print(model)
                try:
                    modelDescription = model[dataModel]["description"]
                    print(len(modelDescription))
                    if len(modelDescription) > 0:
                        make_paragraph("")
                        specContent += make_paragraph(
                            translation("Global description: **" + modelDescription + "**", english, lang, authKey))
                except:
                    nada = 0
                try:
                    version = model[dataModel]["x-version"]
                    print(version)
                    print(type(version))
                    specContent += make_paragraph(translation("version: " + version, english, lang, authKey))
                except:
                    nada = 0
            else:
                print("Not found")
                modelDescription = ""
            specContent += comment_spec("20-Description", False)
            #########################################
            # 3: List of properties               #
            #########################################
            specContent += comment_spec("30-PropertiesList", True)
            specContent += make_paragraph("")
            specContent += translation(listOfPropertiesText, english, lang, authKey) + chr(10)
            specContent += translation(warningTypes, english, lang, authKey) + chr(10)
            specContent += make_paragraph("")

            
            # this is retrieving the full model from the repo.
            schemaUrl = "https://smart-data-models.github.io/" + repoName + "/" + dataModel + "/" + modelYaml
            print(schemaUrl)
            request = requests.get(schemaUrl)
            if request.status_code == 200:

                def list_all_properties(schema, level):
                    if level >= 3: return ""
                    tmpSpecContent = ""
                    for prop in schema["properties"]:
                        # propDict = schema["properties"][prop]
                        partialoutput = ""
                        try:
                            propKeys = list(schema["properties"][prop].keys())

                            if "properties" in propKeys:
                                partialoutput = list_all_properties(schema["properties"][prop], level + 1)

                            if "type" in schema["properties"][prop]:
                                typeProp = "[" + str(schema["properties"][prop]["type"]) + "]"
                            else:
                                typeProp = "[*]"

                            if "format" in schema["properties"][prop]:
                                    typeProp = "[" + str(schema["properties"][prop]["format"]) + "]"

                            if "x-ngsi" in schema["properties"][prop]:
                                if "model" in schema["properties"][prop]["x-ngsi"]:
                                    urlmodel = schema["properties"][prop]["x-ngsi"]["model"]
                                    propmodel = ". Model: [" + urlmodel + "](" + urlmodel + ")"
                                else:
                                    propmodel = ""
                            else:
                                propmodel = ""

                            if "description" in schema["properties"][prop]:
                                propDescription = schema["properties"][prop]["description"]
                                propDescription = translation(propDescription, english, lang, authKey)
                                propertyLine = "- `" + str(prop) + typeProp + "`" + ": " + propDescription + "  " + propmodel
                            else:
                                propertyLine = "- `" + str(prop) + "`" + ": " + "  "
                            tmpSpecContent += propertyLine + chr(13)
                            if partialoutput:
                                tmpSpecContent += "\t" + chr(13).join(partialoutput.split(chr(13))[:-2]).replace(chr(13), "\n"+"\t"*level) + "\n" + partialoutput.split(chr(13))[-1]
                        except:
                            print(prop)
                            
                    return tmpSpecContent
                
                schema = read_yaml(schemaUrl)
                print(schema)
                print("reviewing these " + str(len(schema[dataModel]["properties"])) + " properties")
                tmpSpecContent = list_all_properties(schema[dataModel], 1)
                specContent += tmpSpecContent
            else:
                print("Not found " + modelYaml)
            specContent += comment_spec("30-PropertiesList", False)
            #########################################
            # 3.5: List of required properties      #
            #########################################
            specContent += comment_spec("35-RequiredProperties", True)
            try:
                specContent += make_paragraph(translation(requiredPropertiesHeader, english, lang, authKey))
                orderedRequired = sorted(list(schema[dataModel]["required"]))
                for requiredProperty in orderedRequired:
                    specContent += "- `" + str(requiredProperty) + "`  " + chr(13)
            except:
                specContent += "- " + translation(noRequiredProperties, english, lang, authKey) + "  " + chr(13)
            specContent += comment_spec("35-RequiredProperties", False)
            #########################################
            # 4: Header from notes.yaml             #
            #########################################
            specContent += comment_spec("40-RequiredProperties", True)
            urlNotesFile = urlNotesRoot + "/" + repoName + "/" + dataModel + "/notes.yaml"
            print("urlNotesFile" + "--")
            print(urlNotesFile)
            request = requests.get(urlNotesFile)
            if request.status_code == 200:
                print("Reading notes")
                notes = read_yaml(urlNotesFile)
                print(notes)
            else:
                print("Not found")
                notes = {}
            try:
                print(len(notes["notesHeader"]))
                if len(notes["notesHeader"]) > 0:
                    specContent += make_paragraph(translation(notes["notesHeader"], english, lang, authKey))
            except:
                nada = 0
            specContent += comment_spec("40-RequiredProperties", False)
            #########################################
            # 5: Data model header                  #
            #########################################
            specContent += comment_spec("50-DataModelHeader", True)
            title = translation(techDescriptionOfPropertiesText, english, lang, authKey)
            specContent += make_header(2, title)
            specContent += make_paragraph(translation(alphabeticOrdered, english, lang, authKey))
            specContent += comment_spec("50-DataModelHeader", False)
            ##########################################
            # 6: yaml of the properties              #
            ##########################################
            specContent += comment_spec("60-ModelYaml", True)

            fileUrl = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/" + modelYaml
            pointer = requests.get(fileUrl)
            if pointer.status_code == 200:
                print("found " + modelYaml)
                yamlText = pointer.content.decode('utf-8')
                yamlLines = yamlText.split(chr(10))
                print(yamlLines)
                specContent += "<details><summary><strong>full yaml details</strong></summary>  " + chr(10) + chr(13)
                specContent += "```yaml" + chr(10)
                for line in yamlLines:
                    if len(line) > 0:
                        if line[0] != "#":
                            specContent += line + "  " + chr(10)
                specContent += "```" + chr(10)
                specContent += "</details>  " + chr(10)
            else:
                print("Not found fullModel.yaml")
            specContent += comment_spec("60-ModelYaml", False)
            #########################################
            # 7: Middle notes from notes.yaml       #
            #########################################
            specContent += comment_spec("70-MiddleNotes", True)
            try:
                print(len(notes["notesMiddle"]))
                if len(notes["notesMiddle"]) > 0:
                    specContent += make_paragraph(translation(notes["notesMiddle"], english, lang, authKey))
            except:
                nada = 0
            specContent += comment_spec("70-MiddleNotes", False)
            #########################################
            # 8: Include the examples as quoted     #
            #########################################
            specContent += comment_spec("80-Examples", True)
            exampleStart = "## " + examplePayloads + "  "
            specContent += make_paragraph(translation(exampleStart, english, lang, authKey))
            namesExamples = {}
            namesExamples["NGSI-v2 key-values Example"] = "example.json"
            namesExamples["NGSI-v2 normalized Example"] = "example-normalized.json"
            namesExamples["NGSI-LD key-values Example"] = "example.jsonld"
            namesExamples["NGSI-LD normalized Example"] = "example-normalized.jsonld"
            for exampleType in namesExamples:
                exampleUrl = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + "/examples/" + namesExamples[exampleType]
                echo("exampleURL", exampleUrl)
                if "V2" in exampleType:
                    jsonOption = "JSON"
                else:
                    jsonOption = "JSON-LD"
                if "key-values" in exampleType:
                    option = " using `options=keyValues`"
                else:
                    option = "not using options"

                if exist_page(exampleUrl)[0]:
                    exampleHeader = "#### " + dataModel + " " + exampleType + "  "
                    specContent += make_paragraph(translation(exampleHeader, english, lang, authKey))
                    print(exampleType)

                    exampleText = "Here is an example of a " + dataModel + " in " + jsonOption + " format as " + exampleType[8:18] + ". This is compatible with " + exampleType[:7] + " when " + option + " and returns the context data of an individual entity."
                    specContent += make_paragraph(translation(exampleText, english, lang, authKey))
                    urlExampleFile = urlNotesRoot + "/" + repoName + "/" + dataModel + "/examples/" + namesExamples[
                        exampleType]
                    request = requests.get(urlExampleFile)
                    if request.status_code == 200:
                        print("Reading model")
                        example = request.text
                        print(example)
                        specContent += "<details><summary><strong>show/hide example</strong></summary>  " + chr(10) + chr(13)
                        # specContent += "```json" + chr(10)
                        specContent += make_literal("json", example)
                        # specContent += "```" + chr(10)
                        specContent += "</details>"
                    else:
                        print("Not found example")
                else:
                    exampleText = "Not available the example of a " + dataModel + " in " + jsonOption + " format as " + exampleType[8:18] + ". This is compatible with " + exampleType[:7] + " when " + option + " and returns the context data of an individual entity." + chr(10)
                    specContent += make_paragraph(translation(exampleText, english, lang, authKey))

                echo("exampleText", exampleText)
            specContent += comment_spec("80-Examples", False)
            #########################################
            # 9: Footer from notes.yaml             #
            #########################################
            specContent += comment_spec("90-FooterNotes", True)
            try:
                print(len(notes["notesFooter"]))
                if len(notes["notesFooter"]) > 0:
                    specContent += make_paragraph(translation(notes["notesFooter"], english, lang, authKey))
            except:
                nada = 0
            specContent += comment_spec("90-FooterNotes", False)
            #########################################
            # A : how to deal with units            #
            #########################################
            specContent += comment_spec("95-Units", True)
            specContent += make_paragraph(translation(unitsWarning, english, lang, authKey))
            specContent += comment_spec("95-Units", False)

            #########################################
            # B : General Footer                    #
            #########################################
            specContent += comment_spec("97-LastFooter", True)
            footerContent = "---" + newLine
            footerContent += "[Smart Data Models](https://smartdatamodels.org) +++ [Contribution Manual](https://bit.ly/contribution_manual) +++ [About](https://bit.ly/Introduction_SDM)"
            specContent += footerContent
            specContent += comment_spec("97-LastFooter", False)


            ############################################
            ## remove extra lines from properties list #
            ############################################

            lines = specContent.split(chr(10))
            specContentReviewed = ""
            counter = 0
            for line in lines:
                print("treating line" + str(counter))
                print("-" + line + "-")
                counter += 1
                if not line.isspace():
                    if line == "":
                        nada = 0
                    elif line[0] == "#":
                        specContentReviewed += newLine
                        specContentReviewed += str(line) + "  " + chr(10)
                        specContentReviewed += newLine
                    else:
                        specContentReviewed += line + "  " + chr(10)
            message = "updated " + fullFileName
            print(fullFileName)
            print(specContentReviewed)
            commit = github_push_from_variable(specContentReviewed, repoName, fullFileName, message, globalUser, token)
            print(commit)



