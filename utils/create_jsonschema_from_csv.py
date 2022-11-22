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
#  limitations under the License.
#  Author: alberto.abella@fiware.org
################################################################################

# This program will create a json schema based on a csv payload submitted through a web form
# contact alberto.abella@fiware.org

import requests
import sys
import re

def convert_csv_json(header, csv, separator, quoted):
    # csv is the variable with the csv payload
    # separator is , or ;
    # quoted could have either, "none", "simple" or "double"
    pattern =  chr(10) + "|" + chr(13) 
    lines = re.split(pattern, csv)
    # print("lines")
    # print(lines)
    rawHeader = header.split(separator)
    if quoted == "simple":
        header = [i.replace("'", "") for i in rawHeader]
    elif quoted == "double":
        header = [i.replace(chr(34), "") for i in rawHeader]
    else:
        header = rawHeader

    rawValues = lines[0].split(separator)
    if quoted == "simple":
        values = [i.replace("'", "") for i in rawValues]
    elif quoted == "double":
        values = [i.replace(chr(34), "") for i in rawValues]
    else:
        values = rawValues
    # print("header")
    # print(header)
    # print("values")
    # print(values)
    mergeValues = []
    for item in values:
      try:
        if float(item) == item:
          mergeValues.append(item)
        else:
          mergeValues.append(chr(34) + str(item)+ chr(34))
      except:
        mergeValues.append(chr(34) + str(item)+ chr(34))
    mergeHeader = [chr(34) + i + chr(34) for i in header]
    return dict(zip(mergeHeader, mergeValues))

header = sys.argv[1]
# print(header)
payload = sys.argv[2]
# print(payload)
email = sys.argv[3]
# print(email)
output = convert_csv_json(header, payload, ",", "double")
url = "https://smartdatamodels.org/extra/create_jsonschema_from_payload.php?jsonpayload=" + str(output) + "&mail=" + email

req = requests.get(url)
text = req.text
print(text)

