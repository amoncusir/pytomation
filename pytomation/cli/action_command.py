import argparse
from typing import List, Tuple

from pytomation.app import App
from pytomation.errors import RunnerActionNotFoundError
from pytomation.module import Module


def run(app: App, args: argparse.Namespace) -> None:
    actions = get_module_with_action(args)

    app.find()

    for action in actions:
        action, module = action
        run_command(app, action, module)


def run_command(app: App, action, module_path) -> None:

    app.find()

    try:
        app.run_action_on_module(module_path, action)
    except RunnerActionNotFoundError as e:
        if e.action == "help":
            default_help_module(e.module)
        else:
            raise e


def get_module_with_action(args: argparse.Namespace) -> List[Tuple[str, str]]:
    actions = []

    for action in args.action:
        module, action = action.rsplit(":", 1)
        actions.append((module, action))

    return actions


def default_help_module(module: Module):
    print(module.docs)
