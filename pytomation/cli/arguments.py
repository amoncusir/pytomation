import argparse
from argparse import Namespace
from os import PathLike
from pathlib import Path
from typing import Sequence, Callable

from pytomation.app import App
from pytomation.cli.action_command import run_command
from pytomation.cli.app_factory import build_from_args
from pytomation.cli.verify_command import verify_modules


def arguments(cwd: PathLike, args: Sequence[str] | None) -> Namespace:

    cwd = Path(cwd).resolve() if cwd is not None and Path(cwd).is_dir() else Path.cwd()

    parser = argparse.ArgumentParser(
        description='Local Cluster CLI Tool'
    )

    parser.add_argument('--cwd', action='store',
                        default=cwd,
                        help='Root path to find')

    parser.add_argument('--module-name', action='store',
                        default='lc.module.py',
                        help='module name to find')

    parser.add_argument('-p', '--profile', action='append',
                        default=[], nargs='?',
                        dest='profiles',
                        help='run with specified profile')

    parser.add_argument('--verify', action='store_const',
                        const=verify_modules,
                        dest='func',
                        help='Show information about current module status and parsed options. '
                             'NOTE: To use the root module path, use "" value')

    parser.add_argument('action',
                        action='store',
                        help='Action to run in module')

    parser.add_argument('module',
                        action='store', nargs='?',
                        default='',
                        help='Module path in dot case to run. To default use the root path')

    parser.add_argument('options',
                        action='store', nargs='*',
                        default=[],
                        help='Custom parameters to pass to module and action')

    parser.set_defaults(func=run_command)

    namespace, unknown_args = parser.parse_known_args(args)

    namespace.options.extend(unknown_args)

    return namespace


def main(cwd: PathLike = None, args: Sequence[str] = None, app_inspect: Callable[[App], None] = None) -> int:
    args = arguments(cwd, args)

    if len(args.profiles) == 0:
        args.profiles.append('test')

    app = build_from_args(args)

    if app_inspect is not None:
        app_inspect(app)

    args.func(app, args)

    return 0


if __name__ == '__main__':
    main()
