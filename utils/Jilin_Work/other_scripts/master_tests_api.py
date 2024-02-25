import os
import sys
import pytz
import datetime
from pathlib import Path

tz = pytz.timezone("Europe/Madrid")

def get_now(tz, format="%m%d"):
    now = datetime.datetime.now(tz=tz)
    formatted_date = now.strftime(format) # MMDD
    return formatted_date

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

email = "aa@gmal.com"
testnumber = 0

dataModelListUrl = "https://raw.githubusercontent.com/smart-data-models/data-models/master/specs/AllSubjects/official_list_data_models.json"
repos = open_json(dataModelListUrl)["officialList"]

for repo in repos:
    subject = repo["repoName"]
    # if not (repoName in ["dataModel.GBFS"]): continue
    if (subject in ["dataModel.OCF", "dataModel.EnergyCIM"]): continue 

    dataModels = repo["dataModels"]
    for dataModel in dataModels:

        datamodelRepoUrl = f"https://github.com/smart-data-models/{subject}/tree/master/{dataModel}"

        os.system(f"sudo /usr/bin/python3 /home/fiware/production/tests/master_tests.py {datamodelRepoUrl} {email} {testnumber}")

        # delete the files related
            # test_output_{email}.txt
            # smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck.json
            # smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck_example-normalized.jsonld
            # smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck_example-normalized.json
        # if test_output has failed steps, then keep it in the record

        testOutputPath = Path(f'/var/www/html/extra/mastercheck_output/test_output_{email}.txt')

        if testOutputPath.is_file():

            def extract_and_copy(input_file, output_file):
                try:
                    with open(input_file, 'r') as f:
                        content = f.read()

                        # Find the '2 failed' string and extract the '2'
                        count_index = content.find(' failed,')
                        if count_index != -1:
                            count_start = content.rfind(' ', 0, count_index)
                            count_end = content.find(' ', count_index)
                            failed_count = content[count_start:count_end].strip()

                            # Append the content to the new file
                            if int(failed_count) != 0:
                                with open(output_file, 'a') as new_file:
                                    new_file.write(content)
                except FileNotFoundError:
                    print(f"The file {input_file} does not exist.")

            output_file_path = './output_file.txt'

            extract_and_copy(testOutputPath, output_file_path)

            os.system(f"sudo rm {testOutputPath}")

        masterCheckOutputPath = Path(f'/var/www/html/extra/mastercheck_output/smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck.json')
        if masterCheckOutputPath.is_file():
            os.system(f"sudo rm {masterCheckOutputPath}")

        exampleJsonLDOutputPath = Path(f'/var/www/html/extra/mastercheck_output/smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck_example-normalized.jsonld')
        if exampleJsonLDOutputPath.is_file():
            os.system(f"sudo rm {exampleJsonLDOutputPath}")

        exampleJsonOutputPath = Path(f'/var/www/html/extra/mastercheck_output/smart-data-models.{subject}_master.{dataModel}_{email}_{get_now(tz)}_mastercheck_example-normalized.json')
        if exampleJsonOutputPath.is_file():
            os.system(f"sudo rm {exampleJsonOutputPath}")

