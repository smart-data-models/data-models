# Building Type
This entity contains a harmonised description of a generic building type. This entity is associated with the vertical segments of smart home, smart cities, industry and related IoT applications. The building type includes a hierarchical structure that allows building types to be grouped in a flexible way.

| Attribute Name | Attribute Type | Description | Constraint |
|:--- |:--- |:--- |:---:|
| id | @id | Provides a unique identifier for an instance of the entity either in the form of a URI (i.e. either a publicly accessible URL or a URN). | Mandatory |
| type | @type | Defines the type of the entity. | Mandatory |
| createdAt | TemporalProperty | Indicates the date/ time that the instance of the entity was created in ISO 8601 format. The value of this will be set by the server when the entity was created. | Mandatory |
| modifiedAt | TemporalProperty | Indicates the date/ time when the entity was last modified in ISO 8601 format. The value of this will be set by the server when the entity was modified, if the entity has not been modified it may have a null value. | Optional |
| source | Property | Specifies the URL to the source of this data (either organisation or where relevant more specific source) | Recommended |
| dataProvider | Property | Specifies the URL to information about the provider of this information | Recommended |
| entityVersion | Property | The entity specification version as a number. A version number of 2.0 or later denotes the entity is represented using NGSI-LD | Recommended |
| name | Property | The name of this BuildingType. | Mandatory |
| description | Property | A description for this BuildingType. | Recommended |
| root | Property | A logical indicator that this is the root of a BuildingType hierarchy. True indicates it is the root, false indicates that it is not the root. | Mandatory |
| buildingTypeParent | Relationship | References any higher level Building Type entities that this type is based on. | Optional |
| buildingTypeChildren | Relationship | Reference to child building types i.e. immediately below this entity in the hierarchy. | Optional |

## NGSI-LD Context Definition
The following NGSI-LD context definition applies to the **Building Type** entity

[Download context definition.](../examples/Building-Type-context.jsonld)

```JavaScript
{
    "@context": {
        "source": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/source",
        "dataProvider": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/dataprovider",
        "entityVersion": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/entityversion",
        "name": "https://schema.org/name",
        "description": "https://schema.org/description",
        "root": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/root",
        "buildingTypeParent": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/buildingtypeparent",
        "buildingTypeChildren": "https://www.gsma.com/iot/iot-big-data/ngsi-ld/buildingtypechildren"
    }
}
```
## Example of Building Type Entity
The following is an example instance of the **Building Type** entity

[Download example entity definition.](../examples/Building-Type.jsonld)

```JavaScript
{
    "@context": [
        "https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/coreContext/ngsi-ld-core-context.json",
        "https://raw.githubusercontent.com/GSMADeveloper/NGSI-LD-Entities/master/examples/Building-Type-context.jsonld"
    ],
    "id": "urn:ngsi-ld:BuildingType:57b912ab-eb47-4cd5-bc9d-73abece1f1b3",
    "type": "BuildingType",
    "createdAt": "2017-01-01T01:20:00Z",
    "modifiedAt": "2017-05-04T12:30:00Z",
    "source": "https://source.example.com",
    "dataProvider": "https://provider.example.com",
    "entityVersion": 2.0,
    "name": {
        "type": "Property",
        "value": "House"
    },
    "description": {
        "type": "Property",
        "value": "Standard building type definition for a domestic house"
    },
    "root": {
        "type": "Property",
        "value": false
    },
    "buildingTypeParent": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:BuildingType:4146335f-839f-4ff9-a575-6b4e6232b734"
    },
    "buildingTypeChildren": {
        "type": "Relationship",
        "object": [
            "urn:ngsi-ld:BuildingType:e4291e84-58f8-11e8-84c3-77e4f1f8c4f1",
            "urn:ngsi-ld:BuildingType:a71c7a08-58f9-11e8-a41e-4bcb7249360e",
            "urn:ngsi-ld:BuildingType:afac9bbc-58f9-11e8-b587-1f0d57b81bb4"
        ]
    }
}
```
