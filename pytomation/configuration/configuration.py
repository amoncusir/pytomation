from pydantic import BaseModel, ConfigDict, Field


class Configuration(BaseModel):
    model_config = ConfigDict(frozen=True)
    """
    Contains properties relevant to the **execution process**.
    Like the verbosity level, the parallelization factor, the name of the modules, the module splitter (needed if
    switches the OS), the cache patterns, etc...

    Must not contain properties related to the project, like the root path, name, credentials, etc.

    The current values bay becomes from different inputs and be merged with them.
    """

    module_name: str = Field(default="pytomation.py")
    module_path_splitter: str = Field(default="/")
    verbosity: int = Field(default=0)
