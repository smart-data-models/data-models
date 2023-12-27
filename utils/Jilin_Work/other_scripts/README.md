## Scripts

### __all_datamodels_context_checker.py

Check example jsonld files for all data models whether `@context` exits, return a file called contexts.json with the results

### create_fake_context_via_json_payload.py

Generate fake context information given example json payload, example_payload.json is the input, fake_context.json is the output.

Example of input:
```json
{
  "id": "urn:ngsi-ld:AgriCrop:df72dc57-1eb9-42a3-88a9-8647ecc954b4",
  "type": "AgriCrop1",
  "dateCreated": "2017-01-01T01:20:00Z",
  "dateModified": "2017-05-04T12:30:00Z",
  "name": "Wheat",
  "alternateName": "Triticum aestivum",
  "agroVocConcept": "http://aims.fao.org/aos/agrovoc/c_7951",
  "seeAlso": [
    "https://example.org/concept/wheat",
    "https://datamodel.org/example/wheat"
  ],
  "description": "Spring wheat",
  "relatedSource": [
    {
      "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
      "applicationEntityId": "app:weat"
    }
  ],
  "hasAgriSoil": [
    "urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
    "urn:ngsi-ld:AgriSoil:e8a8389a-edf5-4345-8d2c-b98ac1ce8e2a"
  ],
  "hasAgriFertiliser": [
    "urn:ngsi-ld:AgriFertiliser:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
    "urn:ngsi-ld:AgriFertiliser:380973c8-4d3b-4723-a899-0c0c5cc63e7e"
  ],
  "hasAgriPest": [
    "urn:ngsi-ld:AgriPest:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
    "urn:ngsi-ld:AgriPest:380973c8-4d3b-4723-a899-0c0c5cc63e7e"
  ],
  "plantingFrom": [
    {
      "dateRange": "-09-28/-10-12",
      "description": "Best Season"
    },
    {
      "dateRange": "-10-11/-10-18",
      "description": "Season OK"
    }
  ],
  "harvestingInterval": [
    {
      "dateRange": "-03-21/-04-01",
      "description": "Best Season"
    },
    {
      "dateRange": "-04-02/-04-15",
      "description": "Season OK"
    }
  ],
  "wateringFrequency": "daily"
}
```

Example of output:
```json
{
    "@context": {
        "id": "@id",
        "type": "@type",
        "dateCreated": "https://smartdatamodels.org/dateCreated",
        "dateModified": "https://smartdatamodels.org/dateModified",
        "name": "https://smartdatamodels.org/name",
        "alternateName": "https://smartdatamodels.org/alternateName",
        "agroVocConcept": "https://smartdatamodels.org/jSjTqcZ/agroVocConcept",
        "seeAlso": "https://smartdatamodels.org/seeAlso",
        "description": "http://purl.org/dc/terms/description",
        "relatedSource": "https://smartdatamodels.org/jSjTqcZ/relatedSource",
        "application": "https://smartdatamodels.org/jSjTqcZ/application",
        "applicationEntityId": "https://smartdatamodels.org/jSjTqcZ/applicationEntityId",
        "hasAgriSoil": "https://smartdatamodels.org/jSjTqcZ/hasAgriSoil",
        "hasAgriFertiliser": "https://smartdatamodels.org/jSjTqcZ/hasAgriFertiliser",
        "hasAgriPest": "https://smartdatamodels.org/jSjTqcZ/hasAgriPest",
        "plantingFrom": "https://smartdatamodels.org/jSjTqcZ/plantingFrom",
        "dateRange": "https://smartdatamodels.org/jSjTqcZ/dateRange",
        "harvestingInterval": "https://smartdatamodels.org/jSjTqcZ/harvestingInterval",
        "wateringFrequency": "https://smartdatamodels.org/jSjTqcZ/wateringFrequency"
    }
}
```

### create_schema_via_json_payload.py

Generate json schema given the example json payload, the input file is example_payload.json, and output file is schema.json

Using the same input file as last one, after running the program the output is below:
```json
{
    "$schema": "http://json-schema.org/schema#",
    "$schemaVersion": "0.0.1",
    "modelTags": "",
    "derivedFrom": "",
    "license": "",
    "$id": "https://smart-data-models.github.io/XXXsubjectXXX/XXXdataModelXXX/schema.json",
    "title": "",
    "description": "",
    "type": "object",
    "allOf": [
        {
            "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/GSMA-Commons"
        },
        {
            "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/Location-Commons"
        },
        {
            "properties": {
                "type": {
                    "description": "Property. NGSI Entity type. It has to be AgriCrop1",
                    "enum": [
                        "AgriCrop1"
                    ]
                },
                // ...
                "hasAgriSoil": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Property. "
                    },
                    "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description Reference to the recommended types of soil suitable for growing this crop. Attribute present in data model AgriParcel of subject dataModel.Agrifood with the description Reference to the soil associated with this parcel of land. "
                },
                "hasAgriFertiliser": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Property. "
                    },
                    "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description Reference to the recommended types of fertiliser suitable for growing this crop. "
                },
                "hasAgriPest": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Property. "
                    },
                    "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description Reference to the pests known to attack this crop. "
                },
                "plantingFrom": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "dateRange": {
                                "type": "string",
                                "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description . Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description . "
                            },
                            "description": {
                                "type": "string",
                                "description": "Property. A description of this item"
                            }
                        },
                        "description": "Property. "
                    },
                    "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description A list of the recommended planting interval date(s) for this crop. Specified using ISO8601 repeating date intervals: <br/><br/>**interval, description**<br/><br/>Where **interval** is in the form of **start date/end date**<br/><br/>--MM-DD/--MM-DD<br/><br/>Meaning repeat each year from this start date to this end date. "
                },
                "harvestingInterval": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "dateRange": {
                                "type": "string",
                                "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description . Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description . "
                            },
                            "description": {
                                "type": "string",
                                "description": "Property. A description of this item"
                            }
                        },
                        "description": "Property. "
                    },
                    "description": "Property. Attribute present in data model AgriCrop of subject dataModel.Agrifood with the description A list of the recommended harvesting interval date(s) for this crop. Specified using ISO8601 repeating date intervals: <br/><br/>**interval, description**<br/><br/>Where **interval** is in the form of **start date/end date**<br/><br/>--MM-DD/--MM-DD<br/><br/>Meaning repeat each year from this start date to this end date. "
                },
                "wateringFrequency": {
                    "type": "string",
                    "description": "Property. "
                }
            }
        }
    ],
    "required": [
        "id",
        "type"
    ]
}
```

### master_tests_api.py

The script that runs the data model check service in batch processing, the failure message of the data model will be stored in file output_file.txt

### generate_any_examples.py

The script generates examples from json schema in a data model directory, schema.json files are required for the process. (Remember to change link/path to schema.json file)