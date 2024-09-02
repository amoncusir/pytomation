import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytomation.application.application import Application


class Command:

    @abc.abstractmethod
    def execute(self, application: Application):
        pass
