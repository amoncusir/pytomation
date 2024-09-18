def test_component_generation(capsys, cli):
    cli(":no_dependency")


def test_component_generation_and_action_parameter_inject(capsys, cli):
    cli(":with_dependency")
