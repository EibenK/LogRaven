from core.information_center import InformationCenter
from abc import ABC, abstractmethod


class AgentsInformation(ABC):
    

    @abstractmethod
    def get_agents_health(self):
        pass

    @abstractmethod
    def get_agents_abnormalities(self):
        pass

    @abstractmethod
    def get_agents_logs(self):
        pass

    @abstractmethod
    def get_agents_status(self):
        pass



class AgentsHealth(AgentsInformation):
    

    def __init__(self):
        super().__init__()
    
    def get_agents_health(self):
        pass


class AgentsLogs(AgentsInformation):
    

    def __init__(self):
        super().__init__()

    def get_agents_logs(self):
        pass


class AgentsStatus(AgentsInformation):
    

    def __init__(self):
        super().__init__()

    def get_agents_status(self):
        pass


class AgentsAbnormalities(AgentsInformation):
    

    def __init__(self):
        super().__init__()

    def get_agents_abnormalities(self):
        pass