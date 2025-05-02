from core.information_center import InformationCenter
from abc import ABC, abstractmethod


class SystemInformation(ABC):
    

    @abstractmethod
    def get_system_health(self):
        pass

    @abstractmethod
    def get_system_abnormalities(self):
        pass

    @abstractmethod
    def get_system_logs(self):
        pass

    @abstractmethod
    def get_system_status(self):
        pass



class SystemHealth(SystemInformation):
    

    def __init__(self):
        super().__init__()
    
    def get_system_health(self):
        pass


class SystemLogs(SystemInformation):
    

    def __init__(self):
        super().__init__()

    def get_system_logs(self):
        pass


class SystemStatus(SystemInformation):
    

    def __init__(self):
        super().__init__()

    def get_system_status(self):
        pass


class SystemAbnormalities(SystemInformation):
    

    def __init__(self):
        super().__init__()

    def get_system_abnormalities(self):
        pass