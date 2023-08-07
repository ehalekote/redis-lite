

Date: August 6th, 2023
ADR ID: 1

## Title
Programming language and tech stack selection for the creation of a Redis clone

## Context
- Short timeline
- Goal of this course is to learn about a new technology (Redis) and the SDLC

## Decision
-  Python + Flask

## Status
- Current 

## Consequences
### Pros
-  I am already familiar with the language and have my machine configured to take full advantage of the language and it's community (package manager, virtual environments, etc...)
- Python code has easy to understand syntax and structure
- Flask is a simple and quick to use web framework with reasonable defaults, that will allow me to focus on building the Redis clone
### Cons
- Flask may not be appropriate if I decide to grow the project, and may end up being technical debt if I have to refactor with a more suitable web framework
