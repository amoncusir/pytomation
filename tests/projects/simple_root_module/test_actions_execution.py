from pathlib import Path

from pytomation import cli
from pytomation.cli.arguments import Options


def main_cli(*args: str):
    path = Path(__file__).parent.resolve()
    options = Options(_cwd=path, module_name="pytomation_module.py", verbosity=5)

    cli.main(args, options)


def test_root_module(capsys):

    main_cli(":root")

    captured = capsys.readouterr()

    assert captured.err == "root", "Root module not wrote the word <root> on the standard error output"


def test_apple_module(capsys):

    main_cli("module_apple:apple")

    captured = capsys.readouterr()

    assert captured.err == "apple", "Apple module not wrote the word <apple> on the standard error output"


def test_banana_module(capsys):

    main_cli("module banana:banana")

    captured = capsys.readouterr()

    assert captured.err == "banana", "Banana module not wrote the word <banana> on the standard error output"


def test_spread_task_propagate(capsys):

    main_cli(":spread_action")

    captured = capsys.readouterr()

    assert captured.err == "rootbananaapple", "The modules didn't propagate the action or ran in bad order"
