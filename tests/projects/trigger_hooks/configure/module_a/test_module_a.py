def test_call_in_place_module_with_custom_mod_name(capsys, cli):
    cli(":module")

    captured = capsys.readouterr()

    assert captured.err == "module", "Root module error on dependencies"
