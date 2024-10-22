import argparse
import logging
from typing import List, Tuple

from old.app import App
from pytomation.errors import RunnerActionNotFoundError
from pytomation.module import Module

__logger__ = logging.getLogger(__name__)


def initialize(app: App, args: argparse.Namespace) -> None:
    actions = get_module_with_action(args)

    app.find()

    for group in actions:
        module, action = group
        logging.debug(f"action: {action}, module: {module}")
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
