# Module/Action Type - 2024/09/02 #

## Context

The current implementation and contract definition tries some abstraction about how are defined from the core, as
inheritance of the first, quickly implementation. Now, taking a look about the project's way, I think it doesn't have
any sense any module and action implementation outside of python code. Because something similar is just another
automation tool with some DSL language. And I did not want that.

## Decision

## The `module` and `action` objects will are implemented as python source files

### Why?

Because don't have any sense to be declared in other way, reducing the current complexity of code.

## Consequences

- Refactor these objects.
