import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time

from services.system_information import SystemServicesInformation, SystemService, SystemServiceLogFinder

class TestSystemServicesInformation(unittest.TestCase):
    def setUp(self):
        # Reset the class variables before each test
        SystemServicesInformation._REGISTRY = []
        SystemServicesInformation._SERVICES = []
        SystemServicesInformation._READY_EVENT = threading.Event()
        SystemServicesInformation._INIT_DONE = False

    def test_system_service_dataclass(self):
        """Test SystemService dataclass initialization"""
        service = SystemService(
            name="TestSystem",
            status="Running",
            logs=[]
        )
        self.assertEqual(service.name, "TestSystem")
        self.assertEqual(service.status, "Running")
        self.assertEqual(service.logs, [])

    @patch('wmi.WMI')
    def test_initialization(self, mock_wmi):
        """Test if SystemServicesInformation initializes correctly"""
        # Mock WMI service
        mock_service = MagicMock()
        mock_service.DisplayName = "Test System Service"
        mock_service.Name = "TestSystem"
        mock_service.State = "Running"
        mock_wmi.return_value.Win32_Service.return_value = [mock_service]

        # Initialize the class
        system_info = SystemServicesInformation()
        
        # Verify initialization
        self.assertTrue(SystemServicesInformation._INIT_DONE)
        self.assertTrue(SystemServicesInformation._READY_EVENT.is_set())
        self.assertEqual(len(SystemServicesInformation._SERVICES), 1)

    def test_wait_until_ready(self):
        """Test wait_until_ready method"""
        # Start a thread that will set the event after a short delay
        def set_event():
            time.sleep(0.1)
            SystemServicesInformation._READY_EVENT.set()

        threading.Thread(target=set_event).start()
        
        # This should not block indefinitely
        SystemServicesInformation.wait_until_ready()
        self.assertTrue(SystemServicesInformation._READY_EVENT.is_set())

    def test_register_subclass(self):
        """Test subclass registration"""
        class TestSubclass(SystemServicesInformation):
            pass

        self.assertIn(TestSubclass, SystemServicesInformation._REGISTRY)

    def test_deregister(self):
        """Test deregister method"""
        class TestSubclass(SystemServicesInformation):
            pass

        SystemServicesInformation.deregister(TestSubclass)
        self.assertNotIn(TestSubclass, SystemServicesInformation._REGISTRY)

    def test_get_registered(self):
        """Test get_registered method"""
        class TestSubclass1(SystemServicesInformation):
            pass
        class TestSubclass2(SystemServicesInformation):
            pass

        registered = SystemServicesInformation.get_registered()
        self.assertEqual(len(registered), 2)
        self.assertIn(TestSubclass1, registered)
        self.assertIn(TestSubclass2, registered)

    @patch('win32evtlog.OpenEventLog')
    @patch('win32evtlog.ReadEventLog')
    def test_system_service_log_finder(self, mock_read_event_log, mock_open_event_log):
        """Test SystemServiceLogFinder log acquisition"""
        # Mock event log data
        mock_event = MagicMock()
        mock_event.SourceName = "SystemService"
        mock_event.TimeGenerated.Format.return_value = "2024-01-01"
        mock_event.StringInserts = ["System alert"]
        
        mock_read_event_log.return_value = [mock_event]
        mock_open_event_log.return_value = MagicMock()

        # Create test system service
        system_service = SystemService(
            name="TestSystem",
            status="Running",
            logs=[]
        )

        # Test log acquisition
        SystemServiceLogFinder.acquire_logs(system_service)
        
        # Verify logs were added
        self.assertTrue(len(system_service.logs) > 0)
        self.assertEqual(system_service.logs[0]["source"], "SystemService")

    def test_monitor_services(self):
        """Test monitor_services method"""
        # Create a test service
        service = SystemService(
            name="TestSystem",
            status="Running",
            logs=[]
        )
        SystemServicesInformation._SERVICES = [service]

        # Create a log finder instance and test monitoring
        log_finder = SystemServiceLogFinder()
        with patch('builtins.print') as mock_print:
            log_finder.monitor_services()
            mock_print.assert_called_once()

if __name__ == '__main__':
    unittest.main() 