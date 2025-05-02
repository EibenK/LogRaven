from abc import ABC, abstractmethod


class SystemInformation(ABC):
    
    _REGISTRY = []

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        SystemInformation._REGISTRY.append(cls)

    @classmethod
    def deregister(cls, sub_cls):
        if sub_cls in cls.__subclasses__:
            cls._REGISTRY.remove(sub_cls)
            # put logging here for class that was removed
            return
        # put logging message here for class not in subclasses

    @classmethod
    def get_registered(cls):
        return list(cls._REGISTRY)


class SystemHealth(SystemInformation):
    
    def get_system_health(self):
        return []


class SystemLogs(SystemInformation):
    
    def get_system_logs(self):
        return []


class SystemStatus(SystemInformation):
    
    def get_system_status(self):
        return []


class SystemAbnormalities(SystemInformation):
    
    def get_system_abnormalities(self):
        # unique values
        # unusually high
        # unusually low
        return []