import threading
import time

from concurrent.futures import ThreadPoolExecutor
from services.agents_information import AgentServicesInformation
from services.security_information import SecurityServicesInformation
from services.system_information import SystemServicesInformation


class InformationCenter():
    """ Orchestrator/Supervisor class """
    def __init__(self):
        self.services = []
        
        self.services.extend(AgentServicesInformation.get_registered())
        self.services.extend(SecurityServicesInformation.get_registered())
        self.services.extend(SystemServicesInformation.get_registered())

        self.executor = ThreadPoolExecutor(max_workers=len(self.services))
        self.running = True
        

    def start_monitoring(self):
        for svc in self.services:
            instance = svc()
            instance.wait_until_ready()
            method = getattr(instance, "monitor_services")
            self.executor.submit(self._wrap_func, method, 20)
        

    def _wrap_func(self, func, interval):
        while(self.running):
            func()
            time.sleep(interval)

    def stop(self):
        self.running = False
        self.executor.shutdown(wait=True)

    def get_services(self):
        return self.services

