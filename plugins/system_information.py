import logging
import time
import win32evtlog
import wmi

from abc import ABC
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SystemService:
    name: str
    status: str
    logs: list


class SystemServicesInformation(ABC):

    _SERVICES = []
    _REGISTRY = []
    _INIT_DONE = False

    def __init__(self):
        if SystemServicesInformation._INIT_DONE:
            return
        c = wmi.WMI()
        # performance test start
        start = time.time()
        for service in c.Win32_Service():
            if "system" in service.DisplayName.lower():
                # store as set to refrain from getting duplicates
                system_service = SystemService(
                    name=service.Name,
                    status=service.State,
                    logs=[],
                )
                self.__class__.acquire_logs(system_service)
                self._SERVICES.append(system_service)
        # performance test end and logged
        end = time.time()
        logger.info(f"duration to get system services: {end - start}")
        # will set after first instantiation
        SystemServicesInformation._INIT_DONE = True

    @classmethod
    def acquire_logs(cls, system_service):
        aggregator = []
        for subcls in cls._REGISTRY:
            logger.info(f"acquiring logs from {subcls().__name__}")
            aggregator.append(subcls().acquire_logs(system_service))
        system_service.logs = aggregator

    ''' Register Methods '''

    def __init_subclass__(cls, **kwargs):
        # Instantiates the subclass first.
        super().__init_subclass__(**kwargs)
        # Adds the instance of the subclass into the registry.
        SystemServicesInformation._REGISTRY.append(cls)
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
        return list(cls._REGISTRY)


class SystemServiceLogFinder(SystemServicesInformation):

    # focused on getting information around the system logs
    def acquire_logs(system_services_obj):
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
                        break
                    for event in events:
                        source = str(event.SourceName).lower()
                        if "system" in source:
                            log_entry = {
                                "source": event.SourceName,
                                "timestamp": event.TimeGenerated.Format(),
                                "message": event.StringInserts
                            }
                            system_services_obj.logs.append(log_entry)
            except Exception as e:
                logger.error(f"error reading {logtype} log: {e}")
