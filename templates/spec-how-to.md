# SPEC HOW TO
This file are the rules for accepted spec.md in the smart data models initiative.

## Objectives
- Allow automatic translation of the specs
- Being able to automatically check if the schema of the data model meet the spec

## spec.md structure

datamodel name `i.e Building`
- required: "object" `list required properties of the model`
    - propertyName1
    - propertyName2
- type: ["object"]
- description:  `This is the description (in several lines if required)`
- properties:
    - propertyName1: `reference to other external models. i.e. location`
        - $ref = `link to other spec`
    - propertyName2: `specific property type. i.e. type`
        - x-attr-type: ["EnumProperty", "Relationship", "Property", "Geoproperty] 
        - type: "string"  `Mandatory if not $ref. String is just an example, other values could be number, etc`
        - format: "URL" `optional. Optional to be included for every propery`
        - description: `Mandatory. Description of the property`
    - propertyname3: `complex type`
        - x-attr-type: "Property"
        - x-model: "https://schema.org/openingHours"
        - type: "array"
            - items:
                - type: "object"
                    - properties:
                        - type:
                            - type: "string"
                            - values:
                                - type:
                                    - type: "array"
                                    - items:
                                        - type: "string"
            - externalDocs:
                - url: "https://schema.org/openingHours"
    - propertyName4: `specific property type. i.e. levels`
        - x-attr-type: "Property" 
        - type: "number"  `Mandatory if not $ref. Number is just an example, other values could be string, etc`
        - range: 
        - description: `Mandatory. Description of the property`
It can be included as many properties as needed. All lines of a property has to be single line
indentation has to be respected (4 spaces, tab is not valid)