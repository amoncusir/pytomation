from typing import TYPE_CHECKING, Tuple


if TYPE_CHECKING:
    from pytomation.context import Context
    from pytomation.module import Module


def extract_module_and_action(qualified_action_path, module: 'Module') -> Tuple[str, str]:
    if ':' not in qualified_action_path:
        raise ValueError(f'Invalid qualified action path: {qualified_action_path}')

    if qualified_action_path.startswith(':'):
        return module.name, qualified_action_path[1:]

    return qualified_action_path.rsplit(':')


def depends_on_executor(qualified_action_path: str, context: 'Context'):
    module = context.current_module
    app = context.app

    module_path, action = extract_module_and_action(qualified_action_path, module)

    app.run_action_on_module(module_path, action)

