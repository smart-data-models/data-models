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

# version 0.8
- No longer required the from pysmartdatamodels import pysmartdatamodels. therefore the usual code import line will be:
- import pysmartdatamodels as sdm
- Fix errors in __init__.py
- Extended descriptions in README.md 

# version 0.8.0.1
- Fix errors in __init__.py
- Fix missing packages in dependencies section

# version 0.8.0.1.1
- Changed the example of code (one line was wrong)
- Updated the model assets (attributes, metadata and official list)

# version 0.8.0.2
- Updated the assets because of publication of new data models

# version 0.8.0.8
- Updated the assets because of publication of new data models (1066) till 6-3-26

# version 0.8.0.9
- Refactored __init__.py and utils/__init__.py to use explicit imports instead of wildcard imports
- Updated README.md (contributor count, links, contact)

# version 0.8.0.10
- Synced GitHub master and local/PyPI copies, which had diverged
- Brought in SQL schema generation fixes from GitHub master: quoted identifiers, anyOf support, no more duplicate id column (PRs #93, #94, #95)
- Fixed __all__ in utils/__init__.py to use string names instead of function objects

# version 0.8.0.11
- Fixed __init__.py: the main API functions (generate_sql_schema, load_all_datamodels, etc.) listed in __all__ were never actually imported into the top-level package, so `from pysmartdatamodels import *` and `from pysmartdatamodels import generate_sql_schema` raised AttributeError. Both now work.