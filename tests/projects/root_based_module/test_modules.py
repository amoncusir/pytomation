from pathlib import Path

from pytomation import cli
from pytomation.cli.arguments import Options


def test_root_module():
    options = Options(
        _cwd=Path.cwd() / "tests/projects/root_based_module", module_name="pytomation_module.py", verbosity=5
    )

    cli.main((":test",), options)
