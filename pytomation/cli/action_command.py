import argparse

from pytomation.app import App
from pytomation.errors import RunnerActionNotFoundError
from pytomation.module import Module


def run_command(app: App, args: argparse.Namespace) -> None:
    action = args.action
    module_path = args.module

    app.find()

    try:
        app.run_action_on_module(module_path, action)
    except RunnerActionNotFoundError as e:
        if e.action == 'help':
            default_help_module(e.module)
        else:
            raise e


def default_help_module(module: Module):
    print(module.docs)
