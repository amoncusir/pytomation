def test_root_modules_both_dependency(capsys, cli):
    cli(":create_water")

    captured = capsys.readouterr()

    assert captured.err == "hydrogenoxigen=water", "Root module error on dependencies"


def test_child_modules_dependency_with_specific_order(capsys, cli):
    cli("hydrogen:experiment")

    captured = capsys.readouterr()

    assert captured.err == "lab-hydrogen-explosion", "Child module error on dependencies"


def test_self_module_depends_on_action(capsys, cli):
    cli("hydrogen:print_name")

    captured = capsys.readouterr()

    assert captured.err == "hydrogen", "Module can't self reference"
