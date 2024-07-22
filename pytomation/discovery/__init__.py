from abc import abstractmethod
from typing import List

from pytomation.module import Module


class Discovery:

    @abstractmethod
    def find_modules(self) -> List[Module]:
        pass
