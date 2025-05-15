import logging
import threading
import time
import win32evtlog
import wmi

from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SecurityService:
    name: str
    status: str
    logs: list


class SecurityServicesInformation(ABC):

    _SERVICES = []
    _REGISTRY = []
    _READY_EVENT = threading.Event()
    _INIT_DONE = False

    def __init__(self):
        if SecurityServicesInformation._INIT_DONE:
            return
        c = wmi.WMI()
        # performance test start
        start = time.time()
        for service in c.Win32_Service():
            if "security" in service.DisplayName.lower():
                # store as set to refrain from getting duplicates
                security_service = SecurityService(
                    name=service.Name,
                    status=service.State,
                    logs=[],
                )
                self.__class__.acquire_logs(security_service)
                self._SERVICES.append(security_service)
        # performance test end and logged
        end = time.time()
        logger.info(f"duration to get security services: {end - start:.2f}")
        # will set after first instantiation
        SecurityServicesInformation._READY_EVENT.set()
        SecurityServicesInformation._INIT_DONE = True

    @classmethod
    def wait_until_ready(cls):
        cls._READY_EVENT.wait()

    @classmethod
    def acquire_logs(cls, security_service):
        aggregator = []
        for subcls in cls._REGISTRY:
            logger.info(f"acquiring logs from {subcls().__name__}")
            aggregator.append(subcls().acquire_logs(security_service))
        security_service.logs = aggregator

    ''' Register Methods '''

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        SecurityServicesInformation._REGISTRY.append(cls)
        logger.debug(f"registered subclass: {cls.__name__}")

    @classmethod
    def deregister(cls, sub_cls):
        if sub_cls in cls.__subclasses__:
            cls._REGISTRY.remove(sub_cls)
            logger.debug(f"deregistered subclass: {sub_cls.__name__}")
            return

    @classmethod
    def get_registered(cls):
        logger.debug(f"returning list of registered classes: {cls._REGISTRY}")
        return cls._REGISTRY


class SecurityServiceLogFinder(SecurityServicesInformation):

    # focused on getting information around the security logs
    def acquire_logs(security_service_obj):
        win_evnt_handlers = {
            "Application": win32evtlog.OpenEventLog('localhost', 'Application'),
            "System": win32evtlog.OpenEventLog('localhost', 'System'),
            "Security": win32evtlog.OpenEventLog('localhost', 'Security'),
        }

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

        for logtype, handle in win_evnt_handlers.items():
            try:
                while True:
                    events = win32evtlog.ReadEventLog(handle, flags, 0)
                    if not events:
                        # logs alot
                        # logger.info(f"No events in {logtype} level, security service, {security_service_obj.name}")
                        break
                    for event in events:
                        source = str(event.SourceName).lower()
                        if "security" in source:
                            log_entry = {
                                "source": event.SourceName,
                                "timestamp": event.TimeGenerated.Format(),
                                "message": event.StringInserts
                            }
                            security_service_obj.logs.append(log_entry)
            except Exception as e:
                print(f"error reading {logtype} log: {e}")

    def monitor_services(self):
        for service in SecurityServicesInformation._SERVICES:
            print(service)