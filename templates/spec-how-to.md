# SPEC HOW TO
This file are the rules for accepted spec.md inthe smart data models initiative.

## Objectives
- Allow automatic translation of the specs
- Being able to automatically check if the schema of the data model meet the spec

## spec.md structure

## Schema
[schema](../schema.json)

## Properties
datamodel name
- required: "object" `list required properties of the model`
    - propertyName1
    - propertyName2
- type: ["object"]
- description:  `This is the description (in several lines if required)`
- properties:
    - propertyname1: `reference to other external models`
        - $ref = `link to other spec`
    - propertyname2:
        - x-attr-type: ["EnumProperty", "Relationship", "Property"] `regular type`
        - type: "string"  `Mandatory if not $ref. String is just an example, other values could be number, `
        - format: "URL" `optional. Optional to be included for every propery`
        - description: `Mandatory. Description of the property`
    - propertyname3: `complex type`
        - x-attr-type: "Property"
        - x-model: "https://schema.org/openingHours"
        - type: array
            - items:
                - type: object
                    - properties:
                        - type:
                            - type: string
                            - values:
                                - type:
                                    - type: array
                                    - items:
                                        - type: string
            - externalDocs:
            url: "https://schema.org/openingHours"
    
It can be included as many properties as needed. All lines of a property has to be single line
indentation has to be respected (4 spaces, tab is not valid)

## Open questions:
- How to include references to already defined properties (i.e. locations commons) 

    
