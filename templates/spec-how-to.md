# SPEC HOW TO
This file are the rules for accepted spec.md inthe smart data models initiative.

## Objectives
- Allow automatic translation of the specs
. Being able to automatically check if the schema of the data model meet the spec

## spec.md structure

# [data model name]

## Description (One single line, no CR) 

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
    
It can be included as many properties as needed. all lines No depending of a property name can be mul    
    
