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

# This file run the two tests for a data model submission
# checks that the schema is properly documented
# checks that the keyvalues payload is valid against the defined schema


import sys
import requests

def echo(concept, variable):
    print("*** " + concept + " ***")
    print(variable)
    print("--- " + concept + " ---")

directory = sys.argv[1]
schemaUrl = directory + "/schema.json"
payloadUrl = directory + "/examples/example.json"

urlCheckSchema = "https://smartdatamodels.org/extra/check_schema.php?schemaUrl=" + schemaUrl + "&mail=alberto.abella@fiware.org&test=1"
echo("urlCheckSchema", urlCheckSchema)
pointer = requests.get(urlCheckSchema)
answerCheckSchema = pointer.text
echo("answerCheckSchema", answerCheckSchema)
urlCheckPayload = "https://smartdatamodels.org/extra/validate_payload.php?payloadUrl=" + payloadUrl + "&schemaUrl=" + schemaUrl
echo("urlCheckPayload", urlCheckPayload)
pointer = requests.get(urlCheckPayload)
answerCheckPayload = pointer.text
echo("answerCheckPayload", answerCheckPayload)
