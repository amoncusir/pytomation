import logging
from argparse import Namespace

from pytomation.app import App
from pytomation.discovery.file_discover import FileDiscovery


def build_from_args(args: Namespace) -> App:
    cwd = args.cwd
    module_file_name = args.module_name

    logging.debug(f"CWD: {cwd}")
    logging.debug(f"Module Name: {module_file_name}")

    discovery = FileDiscovery(cwd, module_file_name)
    app = App(discovery)

    app.add_profiles(args.profiles)
    app.add_args(args.options)

    return app
