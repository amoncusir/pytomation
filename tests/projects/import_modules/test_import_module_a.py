def test_import_module_a_from_root(capsys, cli):
    cli(":import_module_a_greetings")

    captured = capsys.readouterr()

    assert captured.err == "hello"
