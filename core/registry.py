from abc import ABC, abstractmethod


class Registry(ABC):
    """ Class for Log Aggregation Using Registry/Abstract Method Patterns """

    _REGISTRY = []

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        Registry._REGISTRY.append(cls)

    @abstractmethod
    def fetch_logs(self): pass

    @classmethod
    def get_parsed_logs(cls):
        aggregated_logs = []
        for subclass in cls._REGISTRY:
            instance = subclass()
            log = instance.fetch_logs()
            aggregated_logs.extend(log)

        return aggregated_logs
