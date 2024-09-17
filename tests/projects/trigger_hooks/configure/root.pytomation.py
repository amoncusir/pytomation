import pytomation
from pytomation.configuration import Configuration


@pytomation.hooks.configure(order=999)
def trigger_on_configure_object(config: Configuration) -> Configuration:
    return config.copy(module_name="custom_mod.py")
