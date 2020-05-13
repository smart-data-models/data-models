# SPEC HOW TO
This file are the rules for accepted spec.md in the smart data models initiative.

## Objectives
- Allow automatic translation of the specs
- Being able to automatically check if the schema of the data model meet the spec

# Instructions
It can be included as many properties as needed. All lines of a property has to be single line
indentation has to be respected (2 spaces, tab is not valid)
Some properties can be define externally, i.e. in shared elements files, then it will be reference through $ref (see example for propertyname1)
@id/id and @type/type are mandatory properties 
The elements in the spec will be documented compatible with OpenAPI 3.0 yaml, but preceded by '- '. See 
This way it will be easily filtered and created  

## spec.md structure

datamodel name `i.e Building`
- required: "object" `list required properties of the model`
  - id `mandatory. Mapped through context into @id`
  - type `mandatory. Mapped through context into @type` 
  - propertyName1
  - propertyName2
- type: ["object"]
- description: `This is the description of the entity (in several lines if required)`
- properties:
  - id: `Mapped through context into @id`
    - x-attr-type: "Property" 
    - type: "string"  `Mandatory`
    - format: "URI" `optional. Optional to be included for every property`
    - description: Entity Identifier
  - type: `Mapped through context into @type`
    - x-attr-type: "Property" 
    - type: "string"  `Mandatory`
    - description: Type of Entity
  - propertyName1: `reference to other external models. i.e. location`
    - $ref = `link to other spec`
  - propertyName2: `Example of relatiohsip`
    - x-attr-type: "Relationship" 
    - type: "string"
    - format: "URI" `This case, relationship is mandatory. Preferably full URI and not relative`
    - description: `Mandatory. Description of the property`
    - propertyName3: `example of array of strings`
      - x-attr-type: "Property" 
      - type: "array"  `Example of Relationship`
          - items:
             - type: "string"
             - properties 
      - format: "URI" `This case, relationship is mandatory.`
      - description: `Mandatory. Description of the property`
  - propertyName4: `specific property type. i.e. type`
    - x-attr-type: `one of ["EnumProperty", "Relationship", "Property", "Geoproperty]` 
    - type: "string"  `Mandatory if not $ref. String is just an example, other values could be number, etc`
    - format: "URL" `optional. Optional to be included for every propery`
    - description: `Mandatory. Description of the property`        
  - propertyname5: `complex type`
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
