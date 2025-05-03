import wmi
from abc import ABC, abstractmethod


class AgentsInformation(ABC):

    _REGISTRY = []
    _AGENTS = []

    def __init__(self):
        c = wmi.WMI()
        for service in c.Win32_Service():
            if "agent" in service.DisplayName.lower():
                # store as set to refrain from getting duplicates
                self._AGENTS.append((service.Name, service.State))

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
    def get_registered(cls) -> list:
        return list(cls._REGISTRY)

    @abstractmethod
    def get_metadata() -> list:
        pass

    @abstractmethod
    def get_log_type() -> str:
        pass


class AgentsHealth(AgentsInformation):

    def get_agents_health(self) -> list:
        return []

    def get_metadata() -> list:
        return []

    def get_log_type() -> str:
        return "focused"


class AgentsLogs(AgentsInformation):

    def get_agents_logs(self) -> list:
        return []

    def get_metadata() -> list:
        return []

    def get_log_type() -> str:
        return "focused"


class AgentsStatus(AgentsInformation):

    def get_agents_status(self) -> str:
        return "healthy"

    def get_metadata() -> list:
        return []

    def get_log_type() -> str:
        return "focused"


class AgentsAbnormalities(AgentsInformation):

    def get_agents_abnormalities(self) -> list:
        # unique values
        # unusually high
        # unusually low
        return []

    def get_metadata() -> list:
        return []

    def get_log_type() -> str:
        return "focused"
