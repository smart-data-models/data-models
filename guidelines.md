# Smart Data Models guidelines

This is a set of guidelines for defining new data models.

Before creating a new data model, [explore the existing ones](https://smartdatamodels.org/index.php/ddbb-of-properties-descriptions/)  or the [quick finder](https://smartdatamodels.org/index.php/list-of-data-models-3/) to be sure there is
already a data model that covers your use case. Recall to use synonyms in your search. E.g. what you might call Public
Transport already exists under UrbanMobility. 

If you are looking for guidelines on adoption of existing data models, please
refer to [How to use Smart Data Models in your projects](https://github.com/smart-data-models/data-models/blob/master/specs/howto.md)
section.

## Syntax

-   Use English terms, preferably American English.
-   Use camel case syntax for attribute names (`camelCase`).
-   Entity Type names must start with a Capital letter, for instance,
    `WasteContainer`.
-   Use names and not verbs for Attributes of type Property, ex. `name`,
    qualifying it when necessary, ex. `totalSpotNumber` or `dateIssued`.
-   Avoid plurals in Attribute names, but state clearly when a list of items
    fits. Ex. `category`.
-   All first level properties defined in the  json schema has to have a description attribute
    
## Reuse

-   Check for the existence of the same Attribute on any of the other models and
    reuse it, in [this resource](http://smartdatamodels.org) if pertinent.
-   It is also available a resource for looking into the descriptions of the different 
    properties. Access to this [resource](https://smartdatamodels.org/index.php/ddbb-of-properties-descriptions/).
-   Have a look at [schema.org](http://schema.org) trying to find a similar term
    with the same semantics.
-   Try to find common used ontologies or existing standards well accepted by
    the Community, or by goverments, agencies, etc. For instance,
    [Open311](http://www.open311.org/) for civic issue tracking or
    [Datex II](http://www.datex2.eu/) for transport systems.

## Payload validation

-   The schemas defined here are aimed to validate key-values representation of the payloads
-   It means that it is possible to have arrays of relationships (something which is not allowed in 
    NGSI-LD, although it could be implemented through the datasetId)

## Data types

-   When possible reuse schema.org data types (`Text`, `Number`, `DateTime`,
    `StructuredValue`, etc.).
-   Remember that `null` is not allowed in NGSI-LD and therefore should be
    avoided as a value.

## Attribute definition

-   Enumerate the allowed values for each attribute. Generally speaking it is a
    good idea to leave it open for applications to extend the list, provided the
    new value is not semantically covered by any of the existing ones.

-   State clearly what attributes are mandatory and what are optional. Remember
    that `null` value should be avoided as it is prohibited in NGSI-LD. The minimum required 
    attributes will make the data models more flexible for other to use them. 
    
-   Internal attributes. In NGSIv2 there are two special attributes created by the system:
    - dateCreated 
    - dateModified
    
    Similarly in NGSI-LD there are two different:
    - createdAt
    - modifiedAt
    
    those attributes **must NOT be included into the definition of the data model** (schema.json)
    but they can appear in the payloads of the examples included.

## Numbers 

-   When a value is a number, when relevant include range limits if they exist. Otherwise do not do it. 

## Units

-   Define a default unit for magnitudes. Normally it will be the unit as stated
    by the International System of Units.

-   If a quantity is expressed in a different unit than the default one, use the
    [unitCode](http://schema.org/unitCode) metadata attribute in NGSI v2.

-   In NGSI-LD the Property `unitCode` is already defined and available to be
    used.
-   The list of UN/CEFACT Common Code (3 characters) can be download from this [page](https://www.unece.org/cefact/codesfortrade/codes_index.html). The list is available directly from [here](https://www.unece.org/fileadmin/DAM/cefact/recommendations/rec20/rec20.zip). 

## Relative values / Percentages

-   Use values between `0` and `1` for relative quantities, which represent
    attribute values such as `relativeHumidity`, `precipitationProbability`,
    etc.

## Modelling location

-   Use `address` attribute for civic locations as per
    [schema.org](http://schema.org/address). You can read the [location-commons](https://github.com/smart-data-models/data-models/blob/master/common-schema.json)

-   Use the `location` Attribute for geographical coordinates. GeoJSON must be
    used for encoding geospatial properties.
    
- There is a shared resource including both at [https://github.com/smart-data-models/data-models/blob/master/common-schema.json](https://github.com/smart-data-models/data-models/blob/master/common-schema.json#Location-Commons)    

## Modelling linked data

-   When an Entity Attribute is used as a link (relationship) to other entities name
       the attribute using a verb (plus optionally an object) such as
        `hasStop`, `operatedBy`, `hasTrip`, etc. This option is the one
        advocated by NGSI-LD, as in NGSI-LD URNs are used to identify entities,
        and NGSI-LD URNs already convey the type of the target entity, for
        instance `urn:ngsi-ld:gtfs:Stop:S123`.

## Date Attributes

-   In NGSI v2 the Attribute type must be `DateTime`.

-   In NGSI-LD, please check the date and time encoding at the
    [NGSI-LD FAQ](https://github.com/smart-data-models/data-models/blob/master/ngsi-ld_howto.md#airquality-in-ngsi-ld-format).

-   Use the `date` prefix for naming entity attributes representing dates (or
    complete timestamps). Ex. `dateLastEmptying`.

-   `dateCreated` in NGSIv2 (`createdAt` in NGSI-LD) must not be used as long as they are internal attributes of the NGSI specification.

-   `dateModified` in NGSIv2 (`modifiedAt` in NGSI-LD) must not be used as long as they are internal attributes of the NGSI specification.

-   `dateCreated` and `dateModified` are special read-only Entity Attributes provided
    off-the-shelf by NGSI implementations. Be careful because they can be
    different than the actual creation or update date of the real world entity
    represented by its corresponding digital entity.

-   When necessary define additional Attributes to capture precisely all the
    details about dates. For instance, to denote the date at which a weather
    forecast was delivered an attribute named `dateIssued` can be used. In that
    particular case just reusing the internal attribute `dateCreated` would be 
    incorrect because the latter would be the creation date of the (digital) entity 
    representing the weather forecast which typically might have a delay.

## Dynamic attributes

-   In NGSI v2 use a metadata attribute named `timestamp` for capturing the last
    update timestamp of a dynamic attribute. Please note that this is the actual
    date at which the measured value was obtained (from a sensor, by visual
    observation, etc.), and that date might be different than the date (metadata
    attribute named `dateModified` as per NGSI v2) at which the attribute of the
    digital entity was updated, as typically there might be delay, specially on
    IoT networks which deliver data only at specific timeslots.

-   In NGSI-LD use the `observedAt` Property to convey timestamps.

## Internationalization (i18N)

There can be certain entity attributes which content is subject to be
internationalized. For instance, the description of a Point of Interest. The
internationalization (i18N) guidelines for the Smart Data Models are defined as
follows:

-   By default, the value of an attribute subject to be internationalized
    _should_ be expressed in **American English** (`en-US`). However there can
    be situations where an English term is not the most common one, for
    instance, the English exonym for the city of Livorno (Italy) is a very
    obscure term, `Leghorn`. In such situations, the common international name
    (`Livorno` in our example) in latin script should be used.

-   There shall always be a term for the original attribute, i.e. it is not
    allowed to have Entity representations which only contain terms associated
    to language variants.

-   [Under revision] For each language variant of an internationalized attribute, there shall be
    an additional Entity Attribute which name shall be in the form:

`<AttributeName>_<LanguageTag>` where `AttributeName` is the original attribute
name and `LanguageTag` shall be a language tag as mandated by
[RFC 5646](https://www.rfc-editor.org/rfc/rfc5646.txt). W3C provides guidelines
on
[how to use language tags](https://www.w3.org/International/articles/language-tags/).

[JSON-LD](https://www.w3.org/TR/json-ld/#string-internationalization) can
facilitate developers to parse internationalized Entity representations, thus
Context Data Producers are encouraged to use JSON-LD (provided that the backing
implementations support it).

When parsing plain JSON content, developers should validate that the
corresponding JSON terms are actually conveying a language variant of an
attribute. For instance, by validating that the term's suffix actually
corresponds to a valid language tag and by checking that the corresponding
original attribute is contained in the entity.

[Under review] Example:

An entity may contain an attribute named `description`. The value of such
attribute shall be expressed in American English. Additionally, it might exist an
attribute named `description_es` used to convey the value of such a
`description` attribute in Spanish.

## Some of the most used attributes

In case of doubt check the existing data models. The full list can be got in the 
[attributes search tool](https://smartdatamodels.org/index.php/ddbb-of-properties-descriptions/) by using an empty string.

-   `name`
-   `alternateName`
-   `description`
-   `serialNumber`
-   `category`
-   `features`
-   `source`
-   `relativeHumidity`
-   `temperature`

## Versioning

FIWARE Foundation, TMForum, OASC and IUDX Smart Data Models Project aim to maintain backwards compatibility, however some
incompatibilities will inevitably occur over time. Data providers may choose to
tag Entities with an additional `schemaVersion` Attribute so that Data Consumers
can behave accordingly. This aligns with the
[https://schema.org/schemaVersion](https://schema.org/schemaVersion) Property
definition.

## How to contribute

Contributions should come in the form of pull requests.
[Fork](https://help.github.com/articles/fork-a-repo/) the repository,
[Create a branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
containing your changes, and proceed with a
[Pull Request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).
[Submit a form](http://smartdatamodels.org/index.php/submit-a-data-model/). Not recommended (larger delay)

Pull Request should be easy to review, so if the model, or the changes you are
proposing are wide, please create different pull requests.

New data models should be added under a folder structured as follows:

    -   `NewModel/`
        -   `doc/`
            -   `spec.md`: A data model description generated automatically based on the schema.json
                e.g.
                [spec.md of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/doc/spec.md).
            -  `spec_XX.md`: A data model description in language XX translated automatically from the original schema.json
            -  `model.yaml`: A file with the technical description of the different attributes of the data model. Generated automatically
            -  `notes.yaml`: An optional file with customization contents for the specification. Optional
            -  `LICENSE.md`: file with the legal permission of use of th data model. It always grant free user, free modification and free share of modifications.
            -  `swagger.yaml`: A file with the specification in open API format for interactive visualization. Generated automatically
            -  `ADOPTERS.yaml`: A file containing use cases of the data models. Optional
        -   `README.md`: Relevant links to access the contents of the data model. (specifications in different languages, links to the examples or to some other sevices based on the data model.)  e.g.
            [README.md of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/README.md)
        -   `schema.json`: The JSON Schema definition, which includes the descriptons of attributes, e.g.
            [schema.json of WeatherObserved](./Weather/WeatherObserved/schema.json)
            
      - `examples/`
        -   `example.json`: One JSON key-values for NGSI v2 example file, e.g.
            [example.json of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/examples/example.json)
        -   `example.jsonld`: One JSON key-values for NGSI-LD example file, e.g.
            [example.json of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/examples/example.jsonld)
        -   `example-normalized.json`: One JSON example file in NGSI v2
            normalized format, e.g.
            [example-normalized.json of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/examples/example-normalized.json)
        -   `example-normalized-ld.jsonld`: One JSON example file in
            **NGSI-LD** normalized format, e.g.
            [example-normalized-ld.jsonld of WeatherObserved](https://github.com/smart-data-models/dataModel.Weather/blob/master/WeatherObserved/examples/example-normalized.jsonld)
            
      - `resources/`. folder with additional contents for customization a data model in case notes.yaml is not enough. i.e. images. Optional

New Subjects containing data  models should be added under a folder structured as follows:

    -   `Subject/`
        -   `README.md`. Contains links and descriptions to the different data models contained in the subject. Generated automatically
        -   `CONTRIBUTORS.yaml`. Contains data of the authors to the different data models contained in the subject. Optional 
        -   `notes.yaml`. Contents for the customization of the Subject README.md. Optional 
        -   `Subject-schema.json`. Schema containing objects used across differente data models. Referenced from there. Optional 
        -   `DataModel1`. Folder containing all the assets for a data model 
        -   `DataModel_incubated`. Folder with a link to where this new data model is being developing. Soon to be available. Optional

## Definitions' section
The section definitions will be included into the subject-schema.json name of the subject.

## $ref values
Whenever possible they will be absolute references in order to provide the ability to use the data models isolated from the rest of documents

## Going through the data models

For a clear explanation on the current use of the data models. Check the [Going through the data models](https://github.com/smart-data-models/data-models/blob/master/specs/howto.md#going-through-a-data-model)
