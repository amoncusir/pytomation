import argparse
import textwrap
import traceback

from pytomation.app import App


def get_module_path(args: argparse.Namespace) -> str:
    return args.action or args.module


def verify_modules(app: App, args: argparse.Namespace) -> None:
    dot_path = get_module_path(args)
    error = None
    module = None

    try:
        app.find()
        module = app.load_module_branch(dot_path)
    except Exception as e:
        traceback.print_exc()
        error = str(e)

    execution_msg = 'All modules have been verified'

    if error is not None:
        execution_msg = f'Error: {error}'

    pretty_modules = 'No modules loaded'

    if module is not None:
        all_modules = module.deep_children
        all_modules[module.name] = module

        pretty_names = []
        for (name, m) in all_modules.items():
            name = name if name != '' else '<root>'
            actions = '|'.join(m.actions)
            docs = m.docs
            pretty_names.append(f'> {name}[{docs}]: {actions}')

        pretty_modules = '\n    '.join(pretty_names)

    module_path_msg = dot_path if dot_path != '' else '<root>'

    message = f'''
    ## Verifying modules ##
    > Active profiles: {app.profiles}
    > Module path: {module_path_msg}

    :: Parameters

    --cwd = {args.cwd}
    --module-name = {args.module_name}

    :: Execution

    {execution_msg}

    :: Loaded Modules

    {pretty_modules}
    '''

    print(textwrap.dedent(message).lstrip())
