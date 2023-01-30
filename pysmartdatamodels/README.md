[![Smart Data Models](https://smartdatamodels.org/wp-content/uploads/2022/01/SmartDataModels_logo.png "Logo")](https://smartdatamodels.org)  

Smart Data Models 
==================

The [Smart Data Models](https://smartdatamodels.org) is a program lead by [4 organizations](https://smartdatamodels.org/index.php/faqs/) with the collaboration of [more than 80](https://smartdatamodels.org/index.php/statistics/) and open to collaboration. It provides multisector agile standardized free and open-licensed data models based either on actual use cases or on adopted open standards.
The data models describe the entities and their attributes to be used in digital twins deployments, data spaces and other smart applications. The data models are grouped in subjects. Each subject is available at a unique repository at [https://smart-data-models.github.com](https://smart-data-models.github.com). Contributions to existing data models can be done there. New ones are drafted in the [incubated repository](https://github.com/smart-data-models/incubated/) once [filled this form](https://smartdatamodels.org/index.php/new-incubated-data-models/) for getting the permissions. [This manual](https://bit.ly/contribution_manual) helps you with the creation. There is a database of [contributors](https://smartdatamodels.org/index.php/contributors/) available. 

This python package includes all the data models and several functions (listed below) to use them in your developments.

Every data model is open licensed and the list of its attributes and every attribute definition is included. Also, there is a function to check if a key values payload complies with a data model.  

If you want to be updated on this package you can join this [mailing list](https://smartdatamodels.org/index.php/developers-list/) (Announcements are sent only when something relevant happens). We love to hear from you at info@smartdatamodels.org

There are several online tools to manage and to create the data models, [generate examples](https://smartdatamodels.org/index.php/generate-a-ngsi-ld-keyvalues-payload-compliant-with-a-data-model/) or to adapt to [existing ontologies](https://smartdatamodels.org/index.php/generate-acontext-based-on-external-ontologies-iris/). See tools menu option at the [home site](https://smartdatamodels.org).

Currently, there are thirteen domains. 
#### [Smart Cities](https://github.com/smart-data-models/SmartCities)
#### [Smart Agrifood](https://smartdatamodels.org/index.php/statistics/)
#### [Smart Water](https://github.com/smart-data-models/SmartWater)
#### [Smart Energy](https://github.com/smart-data-models/SmartEnergy)
#### [Smart Environment](https://github.com/smart-data-models/SmartEnvironment)
#### [Smart Robotics](https://github.com/smart-data-models/SmartRobotics)
#### [Smart Sensoring](https://github.com/smart-data-models/Smart-Sensoring)
#### [Cross sector](https://github.com/smart-data-models/CrossSector)
#### [Smart Aeronautics](https://github.com/smart-data-models/SmartAeronautics)
#### [Smart Destination](https://github.com/smart-data-models/SmartDestination)
#### [Smart Health](https://github.com/smart-data-models/SmartHealth)
#### [Smart Manufacturing](https://github.com/smart-data-models/SmartManufacturing)
#### [Smart Logistics](https://github.com/smart-data-models/SmartLogistics)

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
        - typeNGSI: Whether it is a property, Geoproperty, or relationship
        - modelTags: inherited from the data model tags
        - license: link to the license for the data model
        - schemaVersion: version of the data model
        - type: data type
        - model: when available the reference model for the attribute
        - units: when available the recommended units for the attribute
        - format: either date, or time, or date-time, or URI, etc the format of the attribute
        Parameters:

        Returns:
           array of objects with the description of the subject

3- List all data models. Function list_all_datamodels()

        List the names of the entities defined in the data models.
        Parameters:

        Returns:
        array of strings: data models' names

4- List all subjects. Function list_all_subjects()

        List the names of the subjects (groups of data models). The subject's names define repositories with the name dataModel.subject at the root of the https://smart-data-models.github.com site
          Parameters:

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

9- Give reference units for an attribute. Function attributes_datamodel(subject, datamodel)

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

11- List the NGSI type (Property, Relationship or Geoproperty) of the attribute. Function ngsi_datatype_attribute(subject, datamodel, attribute)

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

12- Print a list of data models attributes separated by a separator. Function print_datamodel(subject, datamodel, separator, meta_attributes)

        Validates a json schema defining a data model.
        Parameters:
          schema_url: url of the schema (public available). (i.e. raw version of a github repo https://raw.githubusercontent.com/smart-data-models/dataModel.Aeronautics/master/AircraftModel/schema.json


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
        - alreadyUsedProperties: It identifies attributes that have already been used in other data models and includes their definition
        - availableProperties: Identifies those attributes which are not already included in any other data model

13- Returns the link to the repository of a subject. Function subject_repolink(subject)

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
          
14- Returns the links to the repositories of a data model name. Function datamodel_repolink(datamodel)

        It returns the direct link to the repository of the subject if it is found and False if not .
        Parameters:
          subject: name of the subject

        Returns:
         if subject is found
           url of the github repository. Example for subject User it returns 'https://github.com/smart-data-models/dataModel.User.git'
         if subject is not found
           False

15- Update the official data model list or the database of attributes from the source. Function update_data()

        It returns an array with the direct links to the repositories where is located the data model if it is found and False if not found.
        Parameters:
          datamodel: name of the data model

        Returns:
         if data model is found
           array of urls (even with one single result) to the github repository. Example for subject Activity it returns ['https://github.com/smart-data-models/dataModel.User.git']
         if data model is not found
           False

## Pending features (glad to receive contributions to them)

A.- Function to allow submission of improvements (i.e. missing recommended units or model) and comments to the different data models. Currently, you can do it searching for your data model here 
[https://smartdatamodels.org/index.php/list-of-data-models-3/](https://smartdatamodels.org/index.php/list-of-data-models-3/) going to the github repo and making your PR or raising your issues there.

B.- Function to submit a new data model to an incubation repository. Currently, this is done manually [incubated repository](https://github.com/smart-data-models/incubated/tree/master). By filling this [form](https://smartdatamodels.org/index.php/new-incubated-data-models/) you are granted to contribute with new data models. For existing data models just see point C    

if you want to suggest other functions / needs please let us know at info@smartdatamodels.org.

### some example code

from pysmartdatamodels import pysmartdatamodels as sdm

subject = "dataModel.Weather"

dataModel = "WeatherForecast"

attribute = "precipitation"

print(sdm.load_all_datamodels())

print(len(sdm.load_all_attributes()))   # there is more than 19.000 to get all listed

print(sdm.list_all_datamodels())

print(sdm.list_all_subjects())

print(sdm.datamodels_subject("dataModel.Weather"))

print(sdm.description_attribute(subject, dataModel, attribute))

print(sdm.datatype_attribute(subject, dataModel, attribute))

print(sdm.model_attribute(subject, dataModel, attribute))

print(sdm.units_attribute(subject, dataModel, attribute))

print(sdm.attributes_datamodel(subject, dataModel))

print(sdm.subject_repolink(subject))

print(sdm.datamodel_repolink(dataModel))

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

sdm.update_data()
