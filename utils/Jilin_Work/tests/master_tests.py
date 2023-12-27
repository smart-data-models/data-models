# input the root of the data model
# browse directories for .py files
# loading in the masters and execute as a single file
# it has a dictionary with the result of every test

import sys
import pytz

from utils.utils import *
from fileStructure import *
from fileContent import *

################################################
# Add configuration
# 
# test_dependency: 
#   - key: the current test
#   - value: the tests need to run before running the current test
#  for example:
#       3: [1, 2], means if you wanna run test 3, you have to pass the test 1 and 2
#  
# config_test.json:
#   contains hyperparameters link to metaschema, timezone, starting test number by default
# 
# system parameters:
#   - datamodelRepoUrl: the url to the github repository of a specific data model 
#   - mail: the email address related to the contributor
#   - lasttestnumber: the test that contributor wants to do, 0 by default which means fully test
################################################

number_to_testname = {
    1: check_fileStructure,
    2: check_FL_schemajson,
    3: check_FL_examples,
    4: check_FL_others
}

testname_to_number = {
    check_fileStructure: 1,
    check_FL_schemajson: 2,
    check_FL_examples: 3,
    check_FL_others: 4
}

test_dependency = {
    1: [],
    2: [1],
    3: [1,2],
    4: [1]
}

configFileName = "/home/fiware/production/tests/config_test.json"
masterTestConfig = open_jsonref(configFileName)
metaSchema = masterTestConfig["metaSchema"]
timezone = masterTestConfig["timezone"]
testnumber = masterTestConfig["testnumber"]

datamodelRepoUrl = sys.argv[1]
mail = sys.argv[2]
lasttestnumber = int(sys.argv[3])

tz = pytz.timezone(timezone)

################################################
# Create output json file for tests
# assume the system paras are correct
################################################

jsonOutput_filepath, output = create_output_json(testnumber, datamodelRepoUrl, mail, tz, metaSchema)

################################################
# Obtain the tests that need to run based on the given test number from contributor
# and the previous tests
################################################

test_state = {}
for key, value in output.items():
    try:
        if int(key) in number_to_testname.keys():
            test_state[key] = value["result"]
    except:
        continue
print(test_state)

def get_need2run_tests(testnumber, test_state):
    def resolve_dependencies(test, visited_tests):
        visited_tests.add(test)
        for dependency in test_dependency[test]:
            if dependency not in visited_tests:
                resolve_dependencies(dependency, visited_tests)

    # Resolve test dependencies and create an ordered list of tests to run
    visited_tests = set()
    if testnumber == 0:
        for test in test_dependency:
            if test not in visited_tests:
                resolve_dependencies(test, visited_tests)
    else:
        resolve_dependencies(testnumber, visited_tests)
    print(visited_tests)
    # get the need-to-run tests based on the test_state
    # the first false 
    need2run_test = visited_tests.copy()
    for test in visited_tests:
        if str(test) in test_state.keys():
            if not test_state[str(test)]:
                # clean the json output
                clean_test_data(jsonOutput_filepath, test)
            else:
                need2run_test.remove(test)
    
    print(need2run_test)
    ordered_test = [number_to_testname[test] for test in need2run_test]
    
    return ordered_test

# get the mapping functions
def run_tests(tests, datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath):
    # Run the tests in the specified order with the given parameter
    test_stats = [len(tests), 0, 0, len(tests)] # [# of all tests, # of passed tests, # of failed tests, # of left tests]
    current_test_state = [True] * len(tests)
    current_test_number = [testname_to_number[test] for test in tests]
    for id, test in enumerate(tests):
        testnumber = testname_to_number[test]
        flag = True
        # compare with test dependency 
        # current test state
        for dp_test in test_dependency[testnumber]:
            if (dp_test in current_test_number) and (not current_test_state[current_test_number.index(dp_test)]):
                flag = False
                break
        if flag:
            if test(datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath):
                test_stats[1] += 1
                test_stats[-1] -= 1
            else:
                current_test_state[id] = False
                test_stats[2] += 1
                test_stats[-1] -= 1
    return test_stats

################################################
# Run the tests and send the sum up message
################################################

test_stats = run_tests(get_need2run_tests(lasttestnumber, test_state), datamodelRepoUrl, tz, testnumber, mail, jsonOutput_filepath)

send_message(testnumber, mail, tz, type=f"{test_stats[0]} tests needed to run, {test_stats[1]} passed, {test_stats[2]} failed, {test_stats[3]} left.\n")
