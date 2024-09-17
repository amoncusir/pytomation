import pytest


def test_circular_dependency(capsys, cli):

    with pytest.raises(SystemExit):
        cli("infinite_import/viki:import_johan_infinite_loop")

    assert False, "Fix the error type!"
