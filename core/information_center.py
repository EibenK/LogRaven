from plugins.agents_information import AgentsInformation
from plugins.system_information import SystemInformation
from plugins.security_information import SecurityInformation

class InformationCenter():
    """ Class for Log Aggregation Using Registry/Abstract Method Patterns """

    _REGISTRY = []

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        InformationCenter._REGISTRY.append(cls)

    @classmethod
    def deregister(cls):
        if cls in InformationCenter.__subclasses__():
            InformationCenter._REGISTRY.remove(cls)
    