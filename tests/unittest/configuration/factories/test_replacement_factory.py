from pathlib import Path

from pytomation.configuration import Configuration
from pytomation.configuration.factories.replacement_factory import (
    IgnoreType,
    ReplacementFactory,
)


def test_replacement_factory_initialization():
    replacement = [("module_name", "new_module.py"), ("verbosity", 2)]
    factory = ReplacementFactory(replacement)

    assert factory.replacement == replacement


def test_replacement_factory_build():
    initial_config = Configuration()
    replacement = [("module_name", "new_module.py"), ("verbosity", 2)]
    factory = ReplacementFactory(replacement)

    new_config = factory.build(initial_config)

    assert new_config.module_name == "new_module.py"
    assert new_config.verbosity == 2
    assert new_config.module_path_splitter == initial_config.module_path_splitter
    assert new_config.call_path == initial_config.call_path
    assert new_config.project_path == initial_config.project_path


def test_replacement_factory_ignore_type():
    initial_config = Configuration()
    replacement = [("module_name", IgnoreType), ("verbosity", 3)]
    factory = ReplacementFactory(replacement)

    new_config = factory.build(initial_config)

    assert new_config.module_name == initial_config.module_name
    assert new_config.verbosity == 3


def test_replacement_factory_all_ignore_type():
    initial_config = Configuration()
    replacement = [
        ("module_name", IgnoreType),
        ("module_path_splitter", IgnoreType),
        ("call_path", IgnoreType),
        ("project_path", IgnoreType),
        ("verbosity", IgnoreType),
    ]
    factory = ReplacementFactory(replacement)

    new_config = factory.build(initial_config)

    assert new_config.module_name == initial_config.module_name
    assert new_config.module_path_splitter == initial_config.module_path_splitter
    assert new_config.call_path == initial_config.call_path
    assert new_config.project_path == initial_config.project_path
    assert new_config.verbosity == initial_config.verbosity


def test_replacement_factory_multiple_replacements():
    initial_config = Configuration()
    replacement = [
        ("module_name", "new_module.py"),
        ("module_path_splitter", "-"),
        ("call_path", Path("/new/call/path")),
        ("project_path", Path("/new/project/path")),
        ("verbosity", 10),
    ]
    factory = ReplacementFactory(replacement)

    new_config = factory.build(initial_config)

    assert new_config.module_name == "new_module.py"
    assert new_config.module_path_splitter == "-"
    assert new_config.call_path == Path("/new/call/path")
    assert new_config.project_path == Path("/new/project/path")
    assert new_config.verbosity == 10


def test_replacement_factory_empty_replacement():
    initial_config = Configuration()
    replacement = []
    factory = ReplacementFactory(replacement)

    new_config = factory.build(initial_config)

    assert new_config.module_name == initial_config.module_name
    assert new_config.module_path_splitter == initial_config.module_path_splitter
    assert new_config.call_path == initial_config.call_path
    assert new_config.project_path == initial_config.project_path
    assert new_config.verbosity == initial_config.verbosity
