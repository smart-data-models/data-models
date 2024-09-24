# Context related files

this file compiles several resources for the creation of customized @context resources for the [Smart Data Models](https://smartdatamodels.org) Program

# Root directory
- common-context.jsonld: It includes those terms which are declared as common in Smart Data Models Program
- config_ontologies.json: It is an example file for including the different vocabularies to be mapped. It includes all the elements in the ontologies_files directory. Mind that the order matters. Those ontologies which are at the beginning of the file have precedence for mapping terms against others. I.e. if the first vocabulary has the term 'name' and the third as well, the first will prevail over the third
- merge_subjects_config.json: This file is an example for including subjects terms in a @context only based on local Smart Data models IRIs. this case is including all subjects in the initiative.  
- merge_subjects_config_example.json: This file is an example for including subjects terms in a @context only based on local Smart Data models IRIs. this case is including only the subjects for Battery, Building, Device and Weather.

## Ontologies_files
Compiles a version with all the potential versions of the different ontologies and vocabularies used for customized @context 