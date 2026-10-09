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

# version 0.8.1.0
- Removed unused sql_type_statement list in generate_sql_schema (dead code, no output change) - fixes #75 / closes PR #78
- Refreshed model-assets/*.json from their canonical sources (official_list_data_models.json, datamodels_metadata.json, smartdatamodels.json), which had been stale since March 2026. Fixed the generation process along the way: dataModel.ROS2 was private, causing every datamodels_metadata.json regeneration to crash before completion; the metadata MongoDB backing smartdatamodels.json was only ~3% populated (32 of 1047 models) and has now been fully backfilled (164,926 documents, all 82 subjects)
- smartdatamodels.json is now shipped gzip-compressed as smartdatamodels.json.gz (~5.4MB vs ~109MB uncompressed, ~20:1 ratio) -- this is the reason for the minor version bump rather than another 0.8.0.x patch: anyone reading model-assets/smartdatamodels.json directly from the installed package (bypassing the documented API) will need to update to the new filename/format. The documented usage (load_all_attributes(), etc.) is unaffected. update_data() now fetches the pre-compressed file directly (~5MB instead of ~110MB)

# version 0.8.1.1
- Fixed generate_sql_schema crashing on multityped attributes (e.g. type: [Property, Relationship]), which loads as a list and isn't hashable for the type-mapping dict lookup -- now falls through to the documented JSON default like any other unrecognized type
- Fixed generate_sql_schema's enum type names colliding across unrelated models that happen to share an enum-valued attribute name (e.g. two different models both having a "status" enum both generated CREATE TYPE status_type) -- now namespaced per entity, matching smart-data-models/data-models#74
- Fixed validate_data_model_schema calling sys.exit() on every error path, which terminated the caller's entire process instead of returning an error. All 7 call sites now return the already-built error dict instead
- Fixed an O(n*m) performance bug in validate_data_model_schema where the ~160,000-entry attributes database was re-read and re-parsed from disk once per non-common attribute in the schema being validated, instead of once
- Added in-memory caching for the three on-disk data files (official_list_data_models.json, smartdatamodels.json.gz, datamodels_metadata.json) -- description_attribute, datatype_attribute, model_attribute, units_attribute, attributes_datamodel, ngsi_datatype_attribute, print_datamodel and others previously re-read and linearly scanned these files on every single call. update_data() now invalidates the caches it would otherwise leave stale
- Removed debug print() statements left in print_datamodel (was printing every row of the full attributes database) and validate_dcat_ap_distribution_sdm
- Fixed __init__.py: list_all_datamodels was never actually importable from the top-level package (from pysmartdatamodels import list_all_datamodels), unlike the similarly-named load_all_datamodels
- Implemented validate_payload(datamodel, subject, payload): previously a stub that didn't validate the payload at all despite its docstring. Now validates the payload is a JSON object, confirms the data model exists in the given subject, checks the "type" attribute matches, runs full JSON Schema validation against the live schema (collecting every error, not just the first), and separately warns -- without failing -- on attributes present in the payload but not defined in the data model. Exported from the top-level package
