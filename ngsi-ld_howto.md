# NGSI-LD HowTo

A tutorial that can complement this howto can be found at
[https://github.com/FIWARE/tutorials.Linked-Data](https://github.com/FIWARE/tutorials.Linked-Data).

## Introduction

The FIWARE NGSI v2 information model has been evolved to better support linked
data (entity relationships), property graphs and semantics (exploiting the
capabilities offered by [JSON-LD](https://json-ld.org/primer/latest/)). This
work has been conducted under the ETSI ISG CIM initiative and has been branded
as
[NGSI-LD](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.01.01_60/gs_CIM009v010101p.pdf).
The main constructs of NGSI-LD are: **Entity**, **Property** and
**Relationship**. NGSI-LD Entities (instances) can be the subject of Properties
or Relationships. In terms of the traditional NGSI v2 data model, Properties can
be seen as the combination of an attribute and its value. Relationships allow to
establish associations between instances using linked data. In practice, they
are conveyed by means of a special NGSI v2 attribute with a special value
(relationship’s `object`), which happens to be a URI which points to another
entity. They are similar to the `ref` attributes recommended by the Data Models
guidelines.

Properties and Relationships can be the subject of other Properties or
Relationships. Thus, in the NGSI-LD information model there are no attribute’s
metadata, but just “properties of properties” or “properties of relationships”.
It is not expected to have infinite graphs, and in practice, only one or two
levels of Property or Relationship “chaining” will happen. Typically, there will
be one, equivalent to the NGSI v2 `metadata` abstraction. NGSI-LD Entities are
represented using JSON-LD, a JSON-based serialization format for Linked Data.
The main advantage of JSON-LD is that it offers the capability of expanding JSON
terms to URIs, so that vocabularies can be used to define terms unambiguously.

## Steps to migrate to JSON-LD

First of all, each Data Model shall have a JSON-LD `@context`, providing an
unambiguous definition by mapping terms to URIs. For practicality reasons, it is
recommended to have a unique `@context` resource, containing all terms, subject
to be used in every Smart Data Model, the same way as
[http://schema.org](http://schema.org) does. The following steps have to be
followed in order to migrate existing NGSI v2 instantiations of the FIWARE Data
Models to NGSI-LD:

-   NGSI v2 entity `id` attributes have to be converted to URIs, preferably
    using the NGSI-LD URN
-   Regular entity attributes have to be converted to JSON-LD nodes of type
    `Property`.
-   `ref` attributes (pointing to other entities) have to be converted to
    JSON-LD nodes of type `Relationship`.
-   The `timestamp` metadata item has to be mapped to the `observedAt` member of
    a Property node.
-   The `unitCode` metadata item has to be mapped to the `unitCode` member of a
    Property node.
-   The NGSI v2 `DateTime` type has to be properly encoded as per the JSON-LD
    rules.
-   The NGSI v2 `geo:json` type has to be renamed to `GeoProperty`.

The FIWARE Community has already provided a simple script to migrate FIWARE NGSI
entity representations to NGSI-LD, see
[normalized2LD.py](https://github.com/FIWARE/data-models/blob/master/tools/normalized2LD.py)

## Example of migration to NGSI-LD

The figure below shows how air quality information at a certain point of
interest can be conveyed using the FIWARE Data Models (involving the entity
types `AirQualityObserved`, `PointOfInterest`) in NGSI v2 format.

### Airquality in NGSI v2 format

```json
{
    "id": "AirQualityObserved:RZ:Obsv4567",
    "type": "AirQualityObserved",
    "dateObserved": {
        "type": "DateTime",
        "value": "2018-08-07T12:00:00"
    },
    "NO2": {
        "type": "Number",
        "value": 22,
        "metadata": {
            "unitCode": {
                "type": "Text",
                "value": "GP"
            }
        }
    },
    "refPointOfInterest": {
        "type": "Reference",
        "value": "PointOfInterest:RZ:MainSquare"
    }
}
```

### PointOfInterest in NGSI v2 format

```json
{
    "id": "PointOfInterest:RZ:MainSquare",
    "type": "PointOfInterest",
    "category": {
        "type": "List",
        "value": ["113"]
    },
    "description": {
        "type": "Text",
        "value": "Beach of RZ"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Point",
            "coordinates": [-8, 44]
        }
    }
}
```

The figure below shows how air quality information, at a certain point of
interest, can be conveyed using the FIWARE Data Models (involving the entity
types `AirQualityObserved`, `PointOfInterest`) in NGSI-LD format. The new
representation has been obtained by applying the conversion rules described
before.

Please note that the FIWARE Data Models `@context` could also be served by
In migration -- [https://fiware.github.io/data-models/context.jsonld](https://fiware.github.io/data-models/context.jsonld) --
and by
In migration -- [https://fiware.github.io/data-models/full-context.jsonld](https://fiware.github.io/data-models/full-context.jsonld). --
The latter includes both the Smart Data Models and the Core `@context`.

### Airquality in NGSI-LD format

```json
{
    "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
    "type": "AirQualityObserved",
    "dateObserved": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2018-08-07T12:00:00Z"
        }
    },
    "NO2": {
        "type": "Property",
        "value": 22,
        "unitCode": "GP"
    },
    "refPointOfInterest": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

### PointOfInterest in NGSI-LD format

```json
{
    "id": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare ",
    "type": "PointOfInterest",
    "category": {
        "type": "Property",
        "value": ["113"]
    },
    "description": {
        "type": "Property",
        "value": "Beach of RZ"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [-8, 44]
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

The content of the JSON-LD `@context` would contain the mappings enumerated
below, plus many others. Observe that `refPointOfInterest` is labelled as an
`@id`, as it is actually pointing to another Entity (linked data). On the other
hand, there are certain terms such as `location` or `unitCode` which are not
included in the `@context`, as they pertain to the Core JSON-LD `@context` which
is always implicit (and **cannot be overwritten**).

```json
{
    "@context": {
        "dateObserved": "http://schema.fiware.org/dateObserved",
        "NO2": "http://schema.fiware.org/NO2",
        "refPointOfInterest": {
            "@type": "@id",
            "@id": "http://schema.fiware.org/refPointOfInterest"
        },
        "category": "http://schema.fiware.org/category",
        "description": "http://schema.org/description"
    }
}
```

## API Examples

### Entity Creation (`application/ld+json`)

Observe that the request MIME type is set to `application/ld+json`. The
`@context` contains two parts: the ETSI Core `@context` and the Smart Data
Models `@context`. The ETSI core `@context` part could have been omitted as it
is always **implicit** (and cannot be overwritten).

Note: When using `application/ld+json` the payload must always contain a
`@context` member.

```
curl -X POST \
  http://localhost:3000/ngsi-ld/v1/entities/ \
  -H 'Content-Type: application/ld+json' \
  -H 'Content-Length: 903' \
  -d '{
    "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "status": {
        "type": "Property",
        "value": "free",
        "observedAt": "2018-09-21T12:00:00Z"
    },
    "category": {
        "type": "Property",
        "value": [
            "onstreet"
        ]
    },
    "refParkingSite": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ParkingSite:santander:daoiz_velarde_1_5"
    },
    "name": {
        "type": "Property",
        "value": "A-13"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [
                -3.80356167695194,
                43.46296641666926
            ]
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}'
```

### Entity Creation (`application/json`)

In this case the payload should not contain any `@context` member, since the
`@context` is conveyed as a `Link` header in the request. It is noteworthy, that
**only one `Link` header pointing to the JSON-LD `@context` is allowed**. That's
why only the Smart Data Models URI `@context` is provided as the target of a
Link header. Remember that the ETSI Core `@context` is always implicit.

Note: If no `Link` header is provided the Entity members will be mapped to the
Default `@context` which implies that they will be under the dummy
`example.org/ngsi-ld` namespace.

```
curl -X POST \
  http://localhost:3000/ngsi-ld/v1/entities/ \
  -H 'Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
  -H 'content-length: 884' \
  -d '{
        "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
        "type": "ParkingSpot",
        "status": {
            "type": "Property",
            "value": "free",
            "observedAt": "2018-09-21T12:00:00Z"
        },
        "category": {
            "type": "Property",
            "value": [
                "onstreet"
            ]
        },
        "refParkingSite": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:ParkingSite:santander:daoiz_velarde_1_5"
        },
        "name": {
            "type": "Property",
            "value": "A-13"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    -3.80356167695194,
                    43.46296641666926
                ]
            }
        }
    }'
```

### Entity Retrieval (`application/ld+json`)

GET requests should **always** contain a `Link` header to the corresponding
`@context`, so that the Broker can be informed of what is the `@context` of a
query or retrieval operation.

_In this case if a `Link` header had not been provided, the resulting JSON
object would have contained long URIs as member keys, and not the short names
that were used when creating the Entity. (as per the `@context` provided)_

Note: Remember that if no `Link` header is provided the default `@context` will
be used. The default `@context` maps every JSON member to the
`http://example.org/ngsi-ld` dummy namespace.

```
curl -X GET \
  http://localhost:3000/ngsi-ld/v1/entities/urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3 \
  -H 'Accept: application/ld+json' \
  -H 'Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
```

Response will contain what is shown below (headers and payload). Observe that
this response does not include any `Link` header as it is indeed
`application/ld+json`, and, therefore, the `@context` is already a payload
member.

```
Content-Type: application/ld+json

{
    "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "status": {
        "type": "Property",
        "value": "free",
        "observedAt": "2018-09-21T12:00:00Z"
    },
    "category": {
        "type": "Property",
        "value": [
            "onstreet"
        ]
    },
    "refParkingSite": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ParkingSite:santander:daoiz_velarde_1_5"
    },
    "name": {
        "type": "Property",
        "value": "A-13"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [
                -3.80356167695194,
                43.46296641666926
            ]
        }
    },
    "@context": [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ]
}
```

### Entity Retrieval (`application/json`)

GET requests should **always** contain a `Link` header to the corresponding
`@context`, so that the Broker can be informed of what is the `@context` of a
query or retrieval operation. In this case if a `Link` header had not been
provided the resulting JSON object would have contained long URIs as member keys
and not the short names that were used when creating the Entity.

Note: If no `Link` header is provided the default `@context` will be used.
Remember that the default `@context` maps every JSON member to the
`http://example.org/ngsi-ld` dummy namespace.

```
curl -X GET \
  http://localhost:3000/ngsi-ld/v1/entities/urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3 \
  -H 'Accept: application/json' \
  -H 'Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
```

Response will contain what is shown below. Observe that this response **does
include** the `Link` header, as it is `application/json`, and, therefore, the
`@context` does not appear as a member of the JSON payload.

```
Content-Type: application/json
Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"

{
    "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
    "type": "ParkingSpot",
    "status": {
        "type": "Property",
        "value": "free",
        "observedAt": "2018-09-21T12:00:00Z"
    },
    "category": {
        "type": "Property",
        "value": [
            "onstreet"
        ]
    },
    "refParkingSite": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ParkingSite:santander:daoiz_velarde_1_5"
    },
    "name": {
        "type": "Property",
        "value": "A-13"
    },
    "location": {
        "type": "GeoProperty",
        "value": {
            "type": "Point",
            "coordinates": [
                -3.80356167695194,
                43.46296641666926
            ]
        }
    }
}
```

### Query Entities (`application/ld+json`)

GET requests should **always** contain a `Link` header to the corresponding
`@context`, so that the Broker can be informed of what is the `@context` of a
query.

_In this case if a `Link` header had not been provided, **there would not have
been query results**, as all the Query terms would have been mapped to the
default `@context` and no matching would have happened._

Note: Remember that if no `Link` header is provided the default `@context` will
be used. The default `@context` maps every JSON member to the
`http://example.org/ngsi-ld` dummy namespace.

```
curl -X GET \
  http://localhost:3000/ngsi-ld/v1/entities/?type=ParkingSpot&q=status==free&attrs=name,location \
  -H 'Accept: application/ld+json' \
  -H 'Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
```

Response will contain what is shown below (headers and payload). Observe that
this response does not include any `Link` header as it is indeed
`application/ld+json`, and, therefore, the `@context` is already a payload
member of the matching Entities. The Core `@context` is referenced and included
for the sake of completeness although in this particular case, as the Smart
Data Models already contains the Core `@context` that could have been omitted.

```
Content-Type: application/ld+json

[
    {
        "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
        "type": "ParkingSpot",
        "name": {
            "type": "Property",
            "value": "A-13"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    -3.80356167695194,
                    43.46296641666926
                ]
            }
        },
        "@context": [
            "https://schema.lab.fiware.org/ld/context",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ]
    }
]
```

### Query Entities (`application/json`)

GET requests should **always** contain a `Link` header to the corresponding
`@context`, so that the Broker can be informed of what is the `@context` of a
query.

_In this case if a `Link` header had not been provided, there would not have
been query results, as all the Query terms would have been mapped to the default
`@context` and no matching would have happened._

Note: If no `Link` header is provided the default `@context` will be used.
Remember that the default `@context` maps every JSON member to the
`http://example.org/ngsi-ld` dummy namespace.

```
curl -X GET \
  http://localhost:3000/ngsi-ld/v1/entities/?type=ParkingSpot&q=status==free&attrs=name,location \
  -H 'Accept: application/json' \
  -H 'Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
```

Response will contain what is shown below. Observe that this response **does
include** the `Link` header, as its MIME type is `application/json`, and,
therefore, the `@context` does not appear as a member of the JSON payload.

```
Content-Type: application/json
Link: <https://schema.lab.fiware.org/ld/context>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"

[
    {
        "id": "urn:ngsi-ld:ParkingSpot:santander:daoiz_velarde_1_5:3",
        "type": "ParkingSpot",
        "name": {
            "type": "Property",
            "value": "A-13"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    -3.80356167695194,
                    43.46296641666926
                ]
            }
        }
    }
]
```