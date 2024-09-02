"""
Command module to allow run actions on pytomation modules

"""

from pytomation.application.application import Application
from pytomation.command.command import Command


class CallAction(Command):

    module_name: str
    action: str
    arguments: dict

    def __init__(self, module_name: str, action: str, arguments: dict):
        self.module_name = module_name
        self.action = action
        self.arguments = arguments

    def execute(self, application: Application):
        pass
