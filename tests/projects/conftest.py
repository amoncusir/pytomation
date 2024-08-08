from pathlib import Path

import pytest

from pytomation.cli import run
from pytomation.cli.arguments import Options


@pytest.fixture(scope="module")
def cli(request):

    def fn(*args: str):
        path = Path(request.module.__file__).parent.resolve()
        options = Options(_cwd=path, module_name="pytomation_module.py", verbosity=5)

        run(args, options)

    return fn
