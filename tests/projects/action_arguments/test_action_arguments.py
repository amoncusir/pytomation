def test_action_context(capsys, cli):
    cli(":action_context")


def test_action_application(capsys, cli):
    cli(":action_application")


def test_action_manager(capsys, cli):
    cli(":action_manager")


def test_action_context_application_manager(capsys, cli):
    cli(":action_context_application_manager")
