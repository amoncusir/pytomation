def test_root_module(capsys, cli):

    cli(":root")

    captured = capsys.readouterr()

    assert captured.err == "root", "Root module not wrote the word <root> on the standard error output"


def test_apple_module(capsys, cli):

    cli("module_apple:apple")

    captured = capsys.readouterr()

    assert captured.err == "apple", "Apple module not wrote the word <apple> on the standard error output"


def test_banana_module(capsys, cli):

    cli("module banana:banana")

    captured = capsys.readouterr()

    assert captured.err == "banana", "Banana module not wrote the word <banana> on the standard error output"


def test_spread_task_propagate(capsys, cli):

    cli(":spread_action")

    captured = capsys.readouterr()

    assert captured.err == "rootbananaapple", "The modules didn't propagate the action or ran in bad order"
