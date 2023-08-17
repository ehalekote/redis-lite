

Date: August 14th, 2023
ADR ID: 2

## Title
Data structure selection for GET/SET command implementation

## Context
- The GET and SET commands only handle strings
- Keys that already have existing values are overwritten

## Decision
- I will use a Hash, implemented as a hash table via Python's dictionary data structure to GET and SET key-value pairs
- Strings will be used for the keys and values

## Status
- Accepted

## Consequences
### Pros
-   Python dictionaries are easy to work with out of the box
    - easily store key value pairs
    - overwrite already existing key value pairs

### Cons
- Not designed with future TTL feature in mind
