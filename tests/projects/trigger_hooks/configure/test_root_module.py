def test_root_with_custom_mod_name(capsys, cli):
    cli(":root")

    captured = capsys.readouterr()

    assert captured.err == "root", "Root module error on dependencies"
