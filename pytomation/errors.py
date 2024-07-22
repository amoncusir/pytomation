from pytomation.module import Module


class RunnerError(Exception):
    pass


class RunnerModuleNotFoundError(RunnerError):
    def __init__(self, module_name):
        super().__init__(f'Module "{module_name}" not found.')
        self.module_name = module_name


class RunnerActionNotFoundError(RunnerError):

    def __init__(self, action: str, module: Module):
        super().__init__(f'Action "{action}" not found in module "{module.name}"')
        self.action = action
        self.module = module
