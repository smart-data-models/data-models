Building type:
  - required:
    - name
    - root
  - type: "Entity"  
   - description: >
      ## Description
      This entity contains a harmonised description of a generic building type. This entity is associated with the vertical segments of smart home, smart cities, industry and related IoT applications. The building type includes a hierarchical structure that allows building types to be grouped in a flexible way.
        
      ## Data Model
  - properties:  
    - id:
      - x-ngsi:
        - type: "Property"
      - type: "string"
      - format: "uri"
    - type:
      - x-ngsi:
        - type: "Property"
      - type: "string"
      - value: "BuildingType"
    - source:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "uri"
      - description: >
         Specifies the URL to the source of this data (either organisation or where relevant more specific source)	
    - dataProvider:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: >
        Specifies the URL to information about the provider of this information  
    - name:
      - x-ngsi:
        - type: "Property"
      - type: "string"
      - description: > 
      The name of this BuildingType
    - root:
      - x-ngsi:
        - type: "Property"
      - type:
        - Boolean
      - description: >
      A logical indicator that this is the root of a BuildingType hierarchy. True indicates it is the root, false indicates that it is not the root
     - buildingTypeParent:
      - x-ngsi:
        - type: "Relationship"
       - type: "string"
       - format: "uri"
       - description:  >
       References any higher level Building Type entities that this type is based on.
     - buildingTypeChildren:
      - x-ngsi:
        - type: "Relationship"
       - type: "string"
       - format: "uri"
       - description:  >
       Reference to child building types i.e. immediately below this entity in the hierarchy.
