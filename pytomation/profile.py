from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Profile:
    """
    specify a profiles to run
    """

    profiles: List[str]

    def __contains__(self, item):
        return item in self.profiles

    def __iter__(self):
        return iter(self.profiles)
