# PyTomation #

> **Under development, alpha preview**. New versions may (and probably) break old implementations.

An advanced, fully hackable automation library written in Python

## Why???

With existing tools like Make, Just, Task, etc., it's difficult to create a complex automation script with many steps
and logic statements. Often, it is easier to write a small script that can later be called by the specific tool.

PyTomatic isn't a build tool; instead, it is a library that helps transform your static project into a dynamic one.

And, of course, it's built with non-Python projects in mind.

## Installation

> TBD

### None-Python project

Currently only recommend the installation using a python project definition. To achieve, create a project using as
example, poetry and add it as a dependency.  

### Python project

Just add in your dependency descriptor:

> Recommend to install as a development dependency in a virtual environment

```toml
[tool.poetry.group.dev]
[tool.poetry.group.dev.dependencies]
pytomation = "^1.0.0"
```

## Example

Check repo: 

## Contribute

### Dependencies

- [Poetry](https://python-poetry.org/)
- [PyEnv](https://github.com/pyenv/pyenv)

### Set up

1. Install python using pyenv (can omit this step in CI environments installing the right py version): `pyenv install`
2. Init poetry: `poetry install`
3. Install pre-commit: `pre-commit install` (inside poetry virtual env)
4. Run pre-commit: `pre-commit run --all-files`
5. Ready!
