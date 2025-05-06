from plugins.agents_information import AgentServicesInformation
from plugins.system_information import SystemServicesInformation
from plugins.security_information import SecurityServicesInformation

class InformationCenter():
    def __init__(self):
        self.registered = []

    def get_registered(self):
        registeries = [
            AgentServicesInformation.get_registered(),
            SystemServicesInformation.get_registered(),
            SecurityServicesInformation.get_registered()
        ]

        for registry in registeries:
            for cls in registry:
                self.registered.append(cls())
        return self.registered
        
