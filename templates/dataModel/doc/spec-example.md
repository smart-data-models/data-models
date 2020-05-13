Building:
  - required:
    - address
    - category
  - type: "object"
    - allOf:
      - $ref: "https://jason-fox.github.io/swagger-datamodel-test/common.yaml#/Common"
      - $ref: "https://jason-fox.github.io/swagger-datamodel-test/common.yaml#/Movable"  
   - description: >
      ## Description
      This entity contains a harmonised description of a Building. This entity is
      associated with the vertical segments of smart homes, smart cities, industry and
      related IoT applications.
        
      This data model has been partially developed in cooperation with mobile
      operators and the [GSMA](https://www.gsma.com/iot/iot-big-data/), compared to
      GSMA data model following changes are introduced:
        
      * The reference to `BuildingType` is removed, since `BuildingType` compared to
        category` attribute does not introduce significant information.
       
      * `category` attribute is required.
        
      * `openingHours` is introduced following schema.org data model to allow
        fine-grained on building opening times. GSMA supported this as free text in
        the `notes` attribute (removed as well).
        
      * `refSubscriptionService` is not supported, since `SubscriptionService` model
        is not supported currently.
        
      ## Data Model

      For a full description of the following attributes refer to GSMA
      [IoT Big Data Harmonised Data Model](https://github.com/GSMADeveloper/NGSI-LD-Entities)
      
  - properties:  
    - address:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/address"
      - $ref: "https://github.com/smart-data-models/data-models/blob/master/common-schema.md#/Address"
    - category:
      - x-ngsi:
        - type: "EnumProperty"
      - type: "string"
      - enum:
        - apartments
        - barn
        - bungalow
        - commercial
        - bakehouse
        - bridge
        - bunker
        - cabin
        - carport
        - cathedral
        - chapel
        - church
        - civic
        - conservatory
        - construction
        - cowshed
        - detached
        - digester
        - dormitory
        - farm
        - farm_auxiliary
        - garage
        - garages
        - garbage_shed
        - grandstand
        - greenhouse
        - hangar
        - industrial
        - hospital
        - house
        - houseboat
        - hotel
        - hut
        - kindergarten
        - kiosk
        - mosque
        - office
        - pavilion
        - parking
        - public
        - residential
        - retail
        - riding_hall
        - roof
        - ruins
        - school
        - shed
        - service
        - stable
        - static_caravan
        - shrine
        - stadium
        - sty
        - synagogue
        - temple
        - terrace
        - train_station
        - transformer_tower
        - transportation
        - university
        - warehouse
        - water_tower
      - description: >
         The categories that this building belongs to
    - containedInPlace :
      - x-ngsi:
        - type: "Relationship"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: The URL this building resides within  
    - dataProvider:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: >
        Specifies the URL to information about the provider of this information  
    - description:
    - x-ngsi:
        - type: "Property"
        - model: "https://uri.etsi.org/ngsi-ld/description"
      - $ref: 'https://jason-fox.github.io/swagger-datamodel-test/common.yaml#/Description'       
    - floorsAboveGround:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/Integer"
      - type: "integer"
      - format: "int32"
      - description: >
            Number of floors above ground within the building
    - floorsBelowGround:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/Integer"
      - type: "integer"
      - format: "int32"
      - description: >
            Number of floors below ground within the building
    - occupier:
      - x-ngsi:
        - type: "Relationship"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: >
            Link to the occupiers of the building
    - openingHours :
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/openingHours"
      - type: array
        - items:
          - type: object
          - properties:
            - type:
              - type: string
                - values:
                  - type: array
                    - items:
                      - type: string
      - externalDocs:
        - url: "https://schema.org/openingHours"  
    - owner:
      - x-ngsi:
       - type: "Relationship"
       - model: "https://schema.org/URL"
    - type: "string"
    - format: "URL"
    - description: >
            The owner of this building
    - refMap:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: >
            The URL holding a map of the building       
    - source:
      - x-ngsi:
        - type: "Property"
        - model: "https://schema.org/Text", "https://schema.org/URL"
      - type: "string"
      - description: >
            A sequence of characters giving the source of the entity data.
    - dataProvider:
      - x-ngsi:
        - type: "Relationship"
        - model: "https://schema.org/URL"
      - type: "string"
      - format: "URL"
      - description: >
        Specifies the URL to information about the provider of this information
    - location:
      - $ref: "https://github.com/smart-data-models/data-models/blob/master/common-schema.md#/Address"
    - containedInPlace:
      - x-ngsi:
        - type: "Property"
      - type: "string"
      
    
        
      