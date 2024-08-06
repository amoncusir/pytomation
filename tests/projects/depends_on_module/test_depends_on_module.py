def test_root_modules_both_dependency(capsys, cli):
    cli(":create_water")

    captured = capsys.readouterr()

    assert captured.err == "hydrogenoxigen=water", "Root module error on dependencies"
