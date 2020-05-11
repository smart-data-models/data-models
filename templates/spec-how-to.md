# SPEC HOW TO
This file are the rules for accepted spec.md inthe smart data models initiative.

## Objectives
- Allow automatic translation of the specs
- Being able to automatically check if the schema of the data model meet the spec

## spec.md structure

# [data model name]

## Description (One single line, no CR) 
This is the description in one single line

## Schema
[schema](../schema.json)

## Properties
- `propertyname`: one line description
    - `type` : Object, String, Number, Boolean, Geopoint, Relationship (only these are valid values). Do not include if it is attribute 
    - `Required`: yes / no
    - `Range`: (i.e 0-1)
    - `Format`: 
    - `Normative` : In case there is one. One single line
    - 
    
It can be included as many properties as needed. All lines of a property has to be single line
property line has to be hyphen, space, `quoted property` : description
Depending lines has to be in the form 4 spaces, hyphen, space, `quoted elelements` : description

## Open questions:
- How to include references to already defined properties (i.e. locations commons) 

    
