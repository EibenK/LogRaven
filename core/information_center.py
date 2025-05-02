from plugins.agents_information import AgentsInformation
from plugins.system_information import SystemInformation
from plugins.security_information import SecurityInformation

class InformationCenter():
    def __init__(self):
        self.registered = []

    def get_registered(self):
        registeries = [
            AgentsInformation.get_registered(),
            SystemInformation.get_registered(),
            SecurityInformation.get_registered()
        ]

        for registry in registeries:
            for cls in registry:
                self.registered.append(cls())
        return self.registered
        
