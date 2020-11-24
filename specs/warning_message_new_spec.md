The new spec is a new format for documenting the Smart Data Models.

It will allow the generation of specifications in several languages

The properties are taken from the schema.json file

It has to be included for every property in the description attribute for every property. 

This also applies for those properties which are referenced through $ref clauses (i.e. those in the root of the subject in the file 'subject'-schema.json)

In order to provide additional service from this description some conventions are agreed:
    
    - The separator between elements in the description is a dot + space '. ' 
    - Start with any of this values(Property, Relationship or Geoproperty)
    - Include when necesary a reference to a model or normative by including `Model:'(link)'` where (link) is the url of link to the model (notice Model start with capital letter)
    - For those properties which can be measured include `Units:'(units)'` where (units) is the description of the units i.e. meters
    - Include also, when available the list of allowed values
 