import argparse
import logging
from argparse import Namespace
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import Callable, Sequence

from pytomation.app import App
from pytomation.cli.action_command import initialize
from pytomation.cli.app_factory import build_from_args
from pytomation.cli.verify_command import verify_modules


@dataclass(frozen=True)
class Options:

    _cwd: PathLike | None = field(default=None)
    module_name: str = field(default="pytomation.py")
    verbosity: int = field(default=0)

    @property
    def cwd(self) -> Path:
        return Path(self._cwd).resolve() if self._cwd is not None and Path(self._cwd).is_dir() else Path.cwd()

    @staticmethod
    def default() -> "Options":
        return Options()


def arguments(options: Options, args: Sequence[str] | None) -> Namespace:
    cwd = options.cwd

    parser = argparse.ArgumentParser(description="Local Cluster CLI Tool")

    parser.add_argument("--cwd", action="store", default=cwd, help="Root path to find")

    parser.add_argument("--verbose", "-v", action="count", default=options.verbosity)

    parser.add_argument(
        "--module-name",
        action="store",
        default=options.module_name,
        help="module name to find",
    )

    parser.add_argument(
        "-p",
        "--profile",
        action="append",
        default=[],
        nargs="?",
        dest="profiles",
        help="run with specified profile",
    )

    parser.add_argument(
        "--verify",
        action="store_const",
        const=verify_modules,
        dest="func",
        help="Show information about current module status and parsed options. "
        'NOTE: To use the root module path, use "" value',
    )

    parser.add_argument(
        "action",
        action="store",
        nargs="+",
        help="Action to run in module with format [module]:action [[module]:action]...",
    )

    parser.add_argument(
        "options",
        action="store",
        nargs="*",
        default=[],
        help="Custom parameters to pass to module and action",
    )

    parser.set_defaults(func=initialize)

    namespace, unknown_args = parser.parse_known_args(args)

    namespace.options.extend(unknown_args)

    return namespace


def set_verbosity(level: int):
    fix_level = (5 - level) * 10
    logging.getLogger().setLevel(fix_level)
    logging.info(f"Log level {logging.getLevelName(fix_level)}")


def run(
    args: Sequence[str] = None,
    options: Options = Options.default(),
    app_inspect: Callable[[App], None] = None,
) -> int:

    args = arguments(options, args)

    set_verbosity(args.verbose)

    if len(args.profiles) == 0:
        args.profiles.append("test")

    app = build_from_args(args)

    if app_inspect is not None:
        app_inspect(app)

    args.func(app, args)

    return 0
