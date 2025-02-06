This directory contains the decentralized method to test new and existing data models

The file [master_tests.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/master_tests.py) executes all the files in the tests directory as long as they are included in this line of code 

   test_files = ["test_valid_json", "test_file_exists", "test_schema_descriptions", "test_schema_metadata", "test_duplicated_attributes"]

so if you create a new test you need to extend this line with your file. Bear in mind these points
1) that the file you create has to have a function with the same name of the file inside. The file [test_schema_descriptions.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/tests/test_schema_descriptions.py) has a function named test_schema_descriptions  
2) Every function returns 3 values. test_name, success, output. test_name is the description of the test run, success is a boolean value indicating if the overall test has been successful. output contains all the messages for the issues or success passed tests in a json format to be easily manageable. 

The file [master_tests.py](https://github.com/smart-data-models/data-models/blob/master/test_data_model/master_tests.py) is invoked this way
'python3 master_tests.py <repo_url_or_local_path> <email> <only_report_errors>' . It expects to have all the tests in the subdirectory tests (like in the repo)
- '<repo_url_or_local_path>'. It is the local path or url for the repository where the data model is located. It does not matter because any case the files are copied locally and removed once the tests has finished. Independently if you are going to test one file or all of them the parameter of the function has to be the root of the directory where the files are located. The expect structure is described in the [contribution manual](https://bit.ly/contribution_manual). In example https://github.com/smart-data-models/dataModel.Weather/tree/master/WeatherObserved
![file structure](data_model_files_structure.png "Data model file structure")
- '<email>' is the email of the user running the test
- '<only_report_errors>' is a boolean (true or 1) to show just only those unsuccessful tests

