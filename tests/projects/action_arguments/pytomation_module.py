from pytomation.action_metadata import action
from pytomation.application import Application
from pytomation.context import Context
from pytomation.module.manager import ModuleManager

# ARGUMENTS = (
#     Context,
#     Application,
#     ModuleManager,
# )
#
#
# def create_actions(args):
#     self_module = sys.modules[__name__]
#
#     for arg in args:
#         fn = None
#         arg_type = arg.__name__
#         fn_name = f"action_{arg_type.lower()}"
#         fn_code = f"def {fn_name}({arg_type.lower()}: {arg_type.lower()}):\n" \
#                   "    assert isinstance({arg_type.lower()}, {arg_type.lower()})\n" \
#                   "fn = {fn_name}"
#         exec(fn_code)
#         self_module.__dict__[fn_name] = action()(fn)


@action()
def action_context(context: Context):
    assert isinstance(context, Context)


@action()
def action_application(app: Application):
    assert isinstance(app, Application)


@action()
def action_manager(manager: ModuleManager):
    assert isinstance(manager, ModuleManager)


@action()
def action_context_application_manager(context: Context, app: Application, manager: ModuleManager):
    assert isinstance(context, Context)
    assert isinstance(app, Application)
    assert isinstance(manager, ModuleManager)
