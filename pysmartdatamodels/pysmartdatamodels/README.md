[![Smart Data Models](https://smartdatamodels.org/wp-content/uploads/2022/01/SmartDataModels_logo.png "Logo")](https://smartdatamodels.org)  

Smart Data Models 
==================

The [Smart Data Models](https://smartdatamodels.org) is a program lead by [4 organizations](https://smartdatamodels.org/index.php/faqs/) with the collaboration of [more than 100](https://smartdatamodels.org/index.php/statistics/) and open to collaboration. It provides multisector agile standardized free and open-licensed data models based either on actual use cases or on adopted open standards.
The data models describe the entities and their attributes to be used in digital twins deployments, data spaces and other smart applications. The data models are grouped in subjects. Each subject is available at a unique repository at [https://github.com/smart-data-models/](https://github.com/smart-data-models/). Contributions to existing data models can be done there. New ones are drafted in the [incubated repository](https://github.com/smart-data-models/incubated/) once [filled this form](https://smartdatamodels.org/index.php/new-incubated-data-models/) for getting the permissions. [This manual](https://bit.ly/contribution_manual) helps you with the creation. There is a database of [contributors](https://smartdatamodels.org/index.php/contributors/) available. 

This python package includes all the data models and several functions (listed below) to use them in your developments.

Every data model is open licensed and the list of its attributes and every attribute definition is included. Also, there is a function to check if a key values payload complies with a data model.  

If you want to be updated on this package you can join this [mailing list](https://smartdatamodels.org/index.php/developers-list/) (Announcements are sent only when something relevant happens). We love to hear from you at info@smartdatamodels.org

There are several online tools to manage and to create the data models, [generate examples](https://smartdatamodels.org/index.php/generate-a-ngsi-ld-keyvalues-payload-compliant-with-a-data-model/) or to adapt to [existing ontologies](https://smartdatamodels.org/index.php/generate-acontext-based-on-external-ontologies-iris/). See tools menu option at the [home site](https://smartdatamodels.org).

Currently, there are thirteen domains. 

**[Smart Cities](https://github.com/smart-data-models/SmartCities)** | **[Smart Agrifood](https://github.com/smart-data-models/SmartAgrifood)** | **[Smart Water](https://github.com/smart-data-models/SmartWater)** | **[Smart Energy](https://github.com/smart-data-models/SmartEnergy)** | 
**[Smart Environment](https://github.com/smart-data-models/SmartEnvironment)** | 
**[Smart Robotics](https://github.com/smart-data-models/SmartRobotics)** | 
**[Smart Sensoring](https://github.com/smart-data-models/Smart-Sensoring)** | 
**[Cross sector](https://github.com/smart-data-models/CrossSector)** | 
**[Smart Aeronautics](https://github.com/smart-data-models/SmartAeronautics)** | 
**[Smart Destination](https://github.com/smart-data-models/SmartDestination)** | 
**[Smart Health](https://github.com/smart-data-models/SmartHealth)** | 
**[Smart Manufacturing](https://github.com/smart-data-models/SmartManufacturing)** | 
**[Smart Logistics](https://github.com/smart-data-models/SmartLogistics)**

### Some example code

```python

from pysmartdatamodels import pysmartdatamodels as sdm

def open_jsonref(fileUrl: str):
    import requests
    import jsonref
    """
    Opens a JSON file given its URL or path and returns the loaded content as a JSON object.
    Capable of parsing JSON file with $ref
    Parameters:
    - file_url (str): The URL or path of the JSON file.
    Returns:
    - dict: The loaded JSON content if successful, none otherwise.
    Example:
    open_jsonref("https://example.com/data.json")
    {...}
    open_jsonref("local_file.json")
    {...}
    open_jsonref("invalid-url")
    None
    """
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            output = jsonref.loads(pointer.content.decode('utf-8'), load_on_repr=True, merge_props=True)
            return output
        except:
            return None
    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return jsonref.loads(file.read(), load_on_repr=True, merge_props=True)
        except:
            return None

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

serverUrl = "https://smartdatamodels.org:1026"

value = 0.5

schemaUrl = "https://smart-data-models.github.io/dataModel.Agrifood/AgriApp/schema.json"

modelYaml = "https://raw.githubusercontent.com/smart-data-models/dataModel.Transportation/master/FareCollectionSystem/model.yaml"

DCATAPExampleUrl = "https://raw.githubusercontent.com/smart-data-models/dataModel.DCAT-AP/master/Distribution/examples/example.json"

content_DCAT = open_jsonref(DCATAPExampleUrl)


# Load all datamodels in a dict like the official list
print("1 : ")
print(sdm.load_all_datamodels())

# Load all attributes in a dict like the official export of attributes
print("2 : ")
print(len(sdm.load_all_attributes()))   # there is more than 155.000 to get all listed

# List all data models
print("3 : ")
print(sdm.list_all_datamodels())

# List all subjects
print("4 : ")
print(sdm.list_all_subjects())

# List the data models of a subject
print("5 : ")
print(sdm.datamodels_subject("dataModel.Weather"))

# List description of an attribute
print("6 : ")
print(sdm.description_attribute(subject, dataModel, attribute))

# List data-type of an attribute
print("7 : ")
print(sdm.datatype_attribute(subject, dataModel, attribute))

# Give reference model for an attribute
print("8 : ")
print(sdm.model_attribute(subject, dataModel, attribute))

# Give reference units for an attribute
print("9 : ")
print(sdm.units_attribute(subject, dataModel, attribute))

# List the attributes of a data model
print("10 : ")
print(sdm.attributes_datamodel(subject, dataModel))

# List the NGSI type (Property, Relationship or Geoproperty) of the attribute
print("11 : ")
print(sdm.ngsi_datatype_attribute(subject, dataModel, attribute))

# Validate a json schema defining a data model
print("12 : ")
print(sdm.validate_data_model_schema(schemaUrl))

# Print a list of data models attributes separated by a separator
print("13 : ")
print(sdm.print_datamodel(subject, dataModel, ",", [
        "property",
        "type",
        "dataModel",
        "repoName",
        "description",
        "typeNGSI",
        "modelTags",
        "format",
        "units",
        "model",
    ]))

# Returns the link to the repository of a subject
print("14 : ")
print(sdm.subject_repolink(subject))

# Return the links to the repositories of a data model name
print("15 : ")
print(sdm.datamodel_repolink(dataModel))

# Update the official data model list or the database of attributes from the source
# It will take a while
print("16 : ")
sdm.update_data()

# Return a fake normalized ngsi-ld format example based on the given json schema
print("17 : ")
print(sdm.ngsi_ld_example_generator(schemaUrl))

# Return a fake key value ngsi-ld format example based on the given json schema
print("18 : ")
print(sdm.ngsi_ld_keyvalue_example_generator(schemaUrl))

# Return a fake geojson feature format example based on the given json schema
print("19 : ")
print(sdm.geojson_features_example_generator(schemaUrl))

# Update a broker compliant with a specific data model, inspired by Antonio Jara
print("20 : ")
print(sdm.update_broker(dataModel, subject, attribute, value, serverUrl=serverUrl, updateThenCreate=True))

# Generate a SQL export based on the model.yaml (yaml export of the schema of a data model)   
print("21 : ")
print(sdm.generate_sql_schema(modelYaml))

# Look for a data model name 
print("22 : ")
print(sdm.look_for_datamodel("WeatherFora", 84))

# retrieve the metadata, context, version, model tags, schema, yaml schema, title, description, $id, required, examples, adopters, contributors and sql export of a data model
print("23 : ")
print(sdm.list_datamodel_metadata(dataModel, subject))

# retrieve the metadata, context, version, model tags, schema, yaml schema, title, description, $id, required, examples, adopters, contributors and sql export of a data model
print("23 : ")
print(sdm.list_datamodel_metadata(dataModel, subject))

print("24:")
print(sdm.validate_dcat_ap_distribution_sdm(content_DCAT))

print("25:")
print(sdm.subject_for_datamodel(dataModel))

```

## Functions available include:

1- Load all datamodels in a dict like the official list. Function load_all_datamodels()

        Returns a dict with all data models with this object structure
        - repoName: The name of the subject
        - repoLink: the link to the repository of the subject
        - dataModels: An array with all the datamodels of this subject
        - domains: an array to the domains that this subject belongs to
        Parameters:
          None

        Returns:
          array of objects with the description of the subject
        

2- Load all attributes in a dict like the official export of attributes. Function load_all_attributes()
 
        Returns an array of objects describing every attribute in the data models
        - _id: identifier of the item
        - property: the name of the attribute
        - dataModel: the data model this attribute is present
        - repoName: the subject this data model belongs to
        - description: the description of the attribute
        - typeNGSI: Whether it is a Property, GeoProperty, or Relationship
        - modelTags: inherited from the data model tags
        - license: link to the license for the data model
        - schemaVersion: version of the data model
        - type: data type
        - model: when available the reference model for the attribute
        - units: when available the recommended units for the attribute
        - format: either date, or time, or date-time, or URI, etc the format of the attribute
        Parameters:
          None

        Returns:
          array of objects with the description of the subject

3- List all data models. Function list_all_datamodels()

        List the names of the entities defined in the data models.
        Parameters:
          None

        Returns:
        array of strings: data models' names

4- List all subjects. Function list_all_subjects()

        List the names of the subjects (groups of data models). The subject's names define repositories with the name dataModel.subject at the root of the https://smart-data-models.github.com site
        Parameters:
          None

        Returns:
          array of strings: subjects' names

5- List the data models of a subject. Function datamodels_subject(subject)

        List the names of the entities defined in the data models.
        Parameters:
          subject: name of the subject

        Returns:
         if subject is found
            array of strings: data models' names belonging to the subject
         if subject is not found
            False

6- List description of an attribute. Function description_attribute(subject, datamodel, attribute)

        List the description of an attribute belonging to a subject and data model.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          attribute: name of the attribute

        Returns:
          if subject, datamodel and attribute are found
            string: attribute's description
          if any of the input parameters is not found
            False

7- List data-type of an attribute. Function datatype_attribute(subject, datamodel, attribute)

        List the data type of an attribute belonging to a subject and data model.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          attribute: name of the attribute

        Returns:
          if subject, datamodel and attribute are found
            string: attribute's data type
          if any of the input parameters is not found
            False

8- Give reference model for an attribute. Function model_attribute(subject, datamodel, attribute)

        List the model of an attribute (when available) belonging to a subject and data model.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          attribute: name of the attribute

        Returns:
          if subject, datamodel and attribute are found
            string: attribute model's URL
          if any of the input parameters is not found or there is not a model
            False

9- Give reference units for an attribute. Function units_attribute(subject, datamodel, attribute)

        List the recommended units of an attribute belonging to a subject and data model.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          attribute: name of the attribute

        Returns:
          if subject, datamodel and attribute are found
            string: acronym/text of the recommended units
          if any of the input parameters is not found or there are not recommended units
            False

10- List the attributes of a data model. Function attributes_datamodel(subject, datamodel)

        List the attributes of a data model (currently only first level ones) .
        Parameters:
          subject: name of the subject
          datamodel: name of the data model

        Returns:
          if subject and datamodel  are found
            array: attribute's names
          if any of the input parameters is not found
            False

11- List the NGSI type (Property, Relationship or GeoProperty) of the attribute. Function ngsi_datatype_attribute(subject, datamodel, attribute)

        List the NGSI data type of an attribute (Property, Relationship or Geoproperty) belonging to a subject and data model.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          attribute: name of the attribute

        Returns:
          if subject, datamodel and attribute are found
            string: NGSI data type
          if any of the input parameters is not found
            False

12- Validate a json schema defining a data model. Function validate_data_model_schema(schemaUrl)

        Validates a json schema defining a data model.
        Parameters:
          schemaUrl: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json)


        Returns:
          object with four elements:
        - documentationStatusofProperties: For each first level attribute lists if the attribute is documented and includes the description (when available). Also the NGSI type if is set and which one is described.
        Example:
            "dateCreated":
                  {
                  "x-ngsi": true,
                  "x-ngsi_text": "ok to Property",
                  "documented": true,
                  "text": "This will usually be allocated by the storage platform.. Entity creation timestamp"
                  },
        - schemaDiagnose: It counts the attributes with right descriptions and those which don't.
        <!-- - alreadyUsedProperties: It identifies attributes that have already been used in other data models and includes their definition
        - availableProperties: Identifies those attributes which are not already included in any other data model -->

13- Print a list of data models attributes separated by a separator. Function print_datamodel(subject, datamodel, separator, meta_attributes)

        Print the different elements of the attributes of a data model separated by a given separator.
        Parameters:
          subject: name of the subject
          datamodel: name of the data model
          separator: string between the different elements printed
          meta_attributes: list of different qualifiers of an attribute
              property: the name of the attribute
              type: the data type of the attribute (json schema basic types)
              dataModel: the data model the attribute belongs to
              repoName: the subject the attribute belongs to
              description: the definition of the attribute
              typeNGSI: the NGSI type, Property, Relationship or Geoproperty
              modelTags: the tags assigned to the data model
              format: For those attributes having it the format, i.e. date-time
              units: For those attributes having it the recommended units, i.e. meters
              model: For those attributes having it the reference model, i.e. https://schema.org/Number

        Returns:
          It prints a version of the attributes separated by the separator listing the meta_attributes specified
            A variable with the same strings
          if any of the input parameters is not found it returns false
            False
          

14- Returns the link to the repository of a subject. Function subject_repolink(subject)

        It returns the direct link to the repository of the subject if it is found and False if not .
        Parameters:
          subject: name of the subject

        Returns:
          if subject is found
            url of the github repository. Example for subject User it returns 'https://github.com/smart-data-models/dataModel.User.git'
          if subject is not found
            False

15- Return the links to the repositories of a data model name. Function datamodel_repolink(datamodel)

        It returns an array with the direct links to the repositories where is located the data model if it is found and False if not found.
        Parameters:
          datamodel: name of the data model

        Returns:
          if data model is found
            array of urls (even with one single result) to the github repository. Example for subject Activity it returns ['https://github.com/smart-data-models/dataModel.User.git']
          if data model is not found
            False

16- Update the official data model list or the database of attributes from the source. Function update_data()

17- Return a fake normalized ngsi-ld format example. Function ngsi_ld_example_generator(schemaUrl)

        It returns a fake normalized ngsi-ld format example based on the given json schema
        Parameters:
          schemaUrl: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json)

        Returns:
          if the input parameter exists and the json schema is a valide json:
              a fake normalized ngsi-ld format example stored in dictionary format
          if there's any problem related to input parameter and json schema:
              False


18- Return a fake key value ngsi-ld format example. Function ngsi_ld_keyvalue_example_generator(schemaUrl)

        It returns a fake key value ngsi-ld format example based on the given json schema
        Parameters:
          schemaUrl: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json)

        Returns:
          if the input parameter exists and the json schema is a valide json:
              a fake key value ngsi-ld format example stored in dictionary format
          if there's any problem related to input parameter and json schema:
              False

19- Return a fake geojson feature format example. Function geojson_features_example_generator(schemaUrl)

        It returns a fake geojson feature format example based on the given json schema
        Parameters:
          schemaUrl: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json)

        Returns:
          if the input parameter exists and the json schema is a valide json:
              a fake geojson feature format example stored in dictionary format
          if there's any problem related to input parameter and json schema:
              False

20- Update a broker compliant with a specific data model, inspired by [Antonio Jara](https://twitter.com/Antonio_Jara). Function update_broker(datamodel, subject, attribute, value, entityId=None, serverUrl=None, broker_folder="/ngsi-ld/v1", updateThenCreate=True)

        Parameters:
          - datamodel: the name of the data model of the SDM (see https://github.com/smart-data-models/data-models/blob/master/specs/AllSubjects/official_list_data_models.json) or this form
          https://smartdatamodels.org/index.php/list-of-data-models-3/
          - subject: the name of the subject, including the prefix dataModel.'subject'
          - attribute: name of the attribute in this data model. The list of available attributes can be found with this form
          https://smartdatamodels.org/index.php/ddbb-of-properties-descriptions/?wdt_column_filter%5B1%5D=WeatherObserved (change WeatherObserved by your data model) or with the function of the pysmartdatamodels sdm.attributes_datamodel(subject, datamodel)
          - value: the value to be updated or inserted
          - entity_id (str): The ID of the entity to update. If left none then the query for the broker is returned
          - serverUrl (str): The URL of the NGSI-LD broker.
          - broker_folder(str): It is supposed that the broker is installed in /ngsi/ld (default) change it if installed other location
          - updateThenCreate: If the updating attribute is nonexistent in the wanting entity, then create the attribute first if updateThenCreate is True, otherwise the operation is illegal

        Returns:
          - An array with two values
          - First the boolean result of the operation True if successful and False if not
          - Second a textual context explanation in every case

21- Generate a PostgreSQL schema SQL script from the model.yaml representation of a Smart Data Model.

      Parameters:
        model_yaml (str): url of the model.yaml file (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/WeatherAlert/model.yaml)

      Returns:
        str: A string containing the PostgreSQL schema SQL script.
    

22- Look for a data model based on a string of text, including approximate search 

      Parameters:
        - datamodel_search_text: piece of string with a text to be searched across the name of the data model of the SDM (It can be a part of the data model name)
        - approx_percentage: optional parameter, in case a non-exact matching is required, percentage of likelikhood between 0 and 100. i.e. 90 means quite similar. Example Weather is 64% similar to WeatherObserved, or 74% to WeatherAlert

    Returns:
        - An array with the values of the matching data models names
    

23- Look for the metadata data models that match the text included

       Parameters:
           - datamodel: Exact name of the data model
           - subject: Exact name of the subject

       Returns:
           - An object  with the metadata available for this data model in the different subjects
                -   version
                i.e. "0.0.2"
                -   modelTags
                i.e. "GreenMov"
                -   title of the data model
                i.e. "Smart Data Models. User Context schema"
                -   $id single link to the schema"
                i.e. https://smart-data-models.github.io/dataModel.User/UserContext/schema.json"
                -   description del data model
                i.e. "Information on the context of an anonymized in a given point in time"
                -   required attributes (array)
                i.e. ["id", "type"]
                -   yamlUrl link to the yaml version of the schema (model.yaml)
                i.e. https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/model.yaml
                -   jsonSchemaUrl link to the schema (schema.json)
                i.e. https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/schema.json"
                -   @context location of the @context of the subject.
                i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/context.jsonld"
                - exampleKeyvaluesJson link to the example in key values for NGSI v2 (json)
                i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example.json"
                 - exampleKeyvaluesJsonld link to the example in key values for NGSI LD (jsonld)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example.jsonld"
                 - exampleNormalizedJson link to the example in normalized for NGSI v2 (json)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example-normalized.json"
                 - exampleNormalizedJsonld link to the example in normalized for NGSI LD (jsonld)
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/examples/example-normalized.jsonld"
                 - sql sql export of the schema.
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/schema.sql"
                 - adopters	list of the adopters of the data model
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/UserContext/ADOPTERS.yaml"
                 - contributors	list of the contributors of the subject
                 i.e. "https://raw.githubusercontent.com/smart-data-models/dataModel.User/master/CONTRIBUTORS.yaml"
           - if the data model is not found it returs False

24.- Validates a DCAT-AP registry by using its conformsTo if the conformsTo points to a smart data model schema

    Parameters:
           json_data: metadata in DCAT-AP distribution format (See https://github.com/smart-data-models/dataModel.DCAT-AP/blob/master/Distribution/schema.json and
           https://semiceu.github.io/DCAT-AP/releases/3.0.0/
                conformsTo: Attribute (Array) with links to the json schemas of SDM
                downloadURL: Public available link to the raw format of the payload

       Returns:
           It prints a version of the attributes separated by the separator listing the meta_attributes specified
           A variable with the same strings
           if any of the input parameters is not found it returns False

25- Look for the subjects corresponding to a data model name  

      Parameters:
           datamodel: name of the data model

       Returns:
           An array (always) if there is only one element with the names of the subjects
           Usually only one element in the array isa returned because there are few clashes in data model names
           False if no subject is found         

## Pending features (glad to receive contributions to them)

A.- Function to allow submission of improvements (i.e. missing recommended units or model) and comments to the different data models. Currently, you can do it searching for your data model here 
[https://smartdatamodels.org/index.php/list-of-data-models-3/](https://smartdatamodels.org/index.php/list-of-data-models-3/) going to the github repo and making your PR or raising your issues there.

B.- Function to submit a new data model to an incubation repository. Currently, this is done manually [incubated repository](https://github.com/smart-data-models/incubated/tree/master). By filling this [form](https://smartdatamodels.org/index.php/new-incubated-data-models/) you are granted to contribute with new data models.     

if you want to suggest other functions/ needs please let us know at info@smartdatamodels.org.


## Acknowledgments

Special thanks to the following contributors:

- [fdrobnic](https://github.com/fdrobnic): Changes for porting to Windows
- [Antonio Jara](https://twitter.com/Antonio_Jara): New function for inserting data into broker
- [María José Bernal](mj.bernal@libelium.com): Necessary extension for function update_broker() to allow updating nonexistent attribute into broker
