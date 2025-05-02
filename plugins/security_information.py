from core.information_center import InformationCenter
from abc import ABC, abstractmethod


class SecurityInformation(ABC):
    

    @abstractmethod
    def get_security_health(self):
        pass

    @abstractmethod
    def get_security_abnormalities(self):
        pass

    @abstractmethod
    def get_security_logs(self):
        pass

    @abstractmethod
    def get_security_status(self):
        pass



class SecurityHealth(SecurityInformation):
    

    def __init__(self):
        super().__init__()
    
    def get_security_health(self):
        pass


class SecurityLogs(SecurityInformation):
    

    def __init__(self):
        super().__init__()

    def get_security_logs(self):
        pass


class SecurityStatus(SecurityInformation):
    

    def __init__(self):
        super().__init__()

    def get_security_status(self):
        pass


class SecurityAbnormalities(SecurityInformation):
    

    def __init__(self):
        super().__init__()

    def get_security_abnormalities(self):
        pass