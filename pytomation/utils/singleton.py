import threading


class Singleton(type):
    _instances = {}
    __lock = threading.Lock()  # Not the best, but enough for the current use

    def __call__(cls, *args, **kwargs):

        # Check if bypass flag is passed, and if so, create a new instance
        bypass_singleton = kwargs.pop("bypass_singleton", False)

        if bypass_singleton:
            return super(Singleton, cls).__call__(*args, **kwargs)

        # Standard singleton behavior
        if cls not in cls._instances:
            cls.__lock.acquire()
            # dic assignation is not an atomic operation
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            cls.__lock.release()

        return cls._instances[cls]

    @classmethod
    def remove_instance(cls, target_cls):

        if target_cls in cls._instances:
            del cls._instances[target_cls]
