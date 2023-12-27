## Subproperty support

**Extended** the functions to support parsing subproperties during the process of datamodel publishing, which includes *generating model.yaml, context.jsonld, specifications, readmes, csv files of examples, term and entity terms, and mongodb storage, mysql migration* 

### File Related

- 10_model.yaml_v13.py: line `94-236`
- 20_create_spec_v11.0.py: line `347-415`
- 25_create_subject_context_V7.py: updated the function `list_all_properties` with function `list_all_properties_v2`
- 30_f_properties_inventory_10.0.py: line `120-324`
- 35_create_term_pages6.0.py: 
- 37_create_entity_pages_v2.0.py: line `80-86` and `199-218`
- 60_generate_datamodel_readmes_v17.0.py: line `140-152` and `165-181` to add new sections in the readme
- Mongdb: updated a new structure of storing property

### Other scripts:

They are all under the folder `/home/fiware/production` start with '__all_datamodels__update_xxx' which is specialized to do batch process on any program above 