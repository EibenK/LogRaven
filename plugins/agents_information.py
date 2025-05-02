from abc import ABC, abstractmethod


class AgentsInformation(ABC):

    _REGISTRY = []

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        AgentsInformation._REGISTRY.append(cls)
        
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


class AgentsHealth(AgentsInformation):
    
    def get_agents_health(self):
        return []


class AgentsLogs(AgentsInformation):

    def get_agents_logs(self):
        return []


class AgentsStatus(AgentsInformation):

    def get_agents_status(self):
        return []


class AgentsAbnormalities(AgentsInformation):

    def get_agents_abnormalities(self):
        # unique values
        # unusually high
        # unusually low
        return []