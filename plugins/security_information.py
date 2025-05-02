from abc import ABC, abstractmethod


class SecurityInformation(ABC):

    _REGISTRY = []

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        SecurityInformation._REGISTRY.append(cls)    

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
    

class SecurityHealth(SecurityInformation):
    
    def get_security_health(self):
        return []
    

class SecurityLogs(SecurityInformation):

    def get_security_logs(self):
        return []


class SecurityStatus(SecurityInformation):

    def get_security_status(self):
        return []


class SecurityAbnormalities(SecurityInformation):

    def get_security_abnormalities(self):
        # unique values
        # unusually high
        # unusually low
        return []