# version 0.6.4
- Included the metadata of every data model in the model_assets_directory
- Included the umber of test in the example code included in the README.md
- requirements need jsonref > 1.0.0
- Included the function look_for_data_model
- Included the function to retrieve the metadata of the data model

# version 0.6.4.1
- Extended the function to retrieve the metadata of the data model to provide the links to the specifications in 8 languages

# version 0.7.0
- Including in the documentation the TODO of the pending functions to be implemented to help forkers to implement some of the functions

# version 0.7.1
- Including new function validate_dcat_ap_distribution_sdm
- Updating the comments of most of the functions
- Some code improvements by jilin.he@fiware.org
- Included a new directory with templates for the creation of a data model. Not used yet but next version they will be used for the creation of local data models. Available at my_subject directory
- Fixing the missing dependency of ruamel.yaml package

# version 0.7.2
- Including a new function to find the subject based on the data model name (In example when only is available the entity type)
- for this function to be shown it has to be included a function to load the content open_jsonref
- Extending the README.md  