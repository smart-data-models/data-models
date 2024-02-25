import json
import asyncio
limit = 30
semaphore = asyncio.Semaphore(n:= limit)

def open_json(fileUrl):
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
    
def extract_subject(url):
    start = url.find("/smart-data-models/") + len("/smart-data-models/")
    end = url.find("/master/")
    return url[start:end]

def extract_datamodel(url, checking_file):
    start = url.find("/master/") + len("/master/")
    end = url.find(f"/examples/")
    return url[start:end]

def get_context_jsonld(repoName):
    # TODO update with the lasted format of context
    return "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/context.jsonld"
    
async def process_expContext(urls, key):
    outputs = []
    repoName, checking_file = key.split(' ')
    for url in urls:
        output = {'message': 'None'}
        output['Subject'] = extract_subject(url)
        output['DataModel'] = extract_datamodel(url, checking_file)  
        output['File'] = checking_file
        
        try:
            expJsonId = open_json(url)      
            if contextKey in expJsonId.keys():
                unverifiedUrls = expJsonId[contextKey]
                # if len(unverifiedUrls) < 2:
                #     print(f"Doesn't have less than one link in the example!")
                if get_context_jsonld(repoName) != unverifiedUrls[-1]:
                    # print(f"Doesn't have right link in the example!")
                    output['message'] = CHECK_CASE[2]
                # else:
                #     print(f"Done!")
            else:
                # print(f"Doesn't have context in the example!")
                output['message'] = CHECK_CASE[1]
        except:
            # print(f"Error")
            output['message'] = CHECK_CASE[0]
        outputs.append(output)
    return outputs
    
urlDataModelsList = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
dataModelsList = open_json(urlDataModelsList)["officialList"]

# rooturl ="/var/www/html/extra"
rooturl = "./"

###########################
#     context.jsonld      #
###########################

# exclude subjects dataModel.EnergyCIM
contextUrlsDict = {}

for checking_file in ['example.jsonld', 'example-normalized.jsonld']:
    for repo in dataModelsList:
        repoName = repo["repoName"]
        if repoName == 'dataModel.EnergyCIM': continue
        contextUrl = get_context_jsonld(repoName)
        expContexts = []
        # now the example context
        for dataModel in repo["dataModels"]:
            expContextUrl = "https://raw.githubusercontent.com/smart-data-models/" + repoName + "/master/" + dataModel + f"/examples/{checking_file}"
            expContexts.append(expContextUrl)
        contextUrlsDict[repoName+f" {checking_file}"] = expContexts

###########################
#   check the validity    #
###########################
CHECK_CASE = ['Error', 'No Context', 'Context not match']
contextKey = '@context'
results = []

for idx, (key, exps) in enumerate(contextUrlsDict.items()):
    # if idx > 30:
    #     break
    print(f"idx: {idx}")
    result = asyncio.run(process_expContext(exps, key))
    results += result

print(len(results))
resultsDict = {k: [] for k in CHECK_CASE}
for res in results:
    if res['message'] in resultsDict.keys():
        resultsDict[res['message']].append({'Subject': res['Subject'], 'DataModel': res['DataModel'], 'File': res['File']})

with open(rooturl + "contexts.json", "w") as file:
    json.dump(resultsDict, file, default=str)
