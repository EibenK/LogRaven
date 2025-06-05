import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time

from services.security_information import SecurityServicesInformation, SecurityService, SecurityServiceLogFinder

class TestSecurityServicesInformation(unittest.TestCase):
    def setUp(self):
        # Reset the class variables before each test
        SecurityServicesInformation._REGISTRY = []
        SecurityServicesInformation._SERVICES = []
        SecurityServicesInformation._READY_EVENT = threading.Event()
        SecurityServicesInformation._INIT_DONE = False

    def test_security_service_dataclass(self):
        """Test SecurityService dataclass initialization"""
        service = SecurityService(
            name="TestSecurity",
            status="Running",
            logs=[]
        )
        self.assertEqual(service.name, "TestSecurity")
        self.assertEqual(service.status, "Running")
        self.assertEqual(service.logs, [])

    @patch('wmi.WMI')
    def test_initialization(self, mock_wmi):
        """Test if SecurityServicesInformation initializes correctly"""
        # Mock WMI service
        mock_service = MagicMock()
        mock_service.DisplayName = "Test Security Service"
        mock_service.Name = "TestSecurity"
        mock_service.State = "Running"
        mock_wmi.return_value.Win32_Service.return_value = [mock_service]

        # Initialize the class
        security_info = SecurityServicesInformation()
        
        # Verify initialization
        self.assertTrue(SecurityServicesInformation._INIT_DONE)
        self.assertTrue(SecurityServicesInformation._READY_EVENT.is_set())
        self.assertEqual(len(SecurityServicesInformation._SERVICES), 1)

    def test_wait_until_ready(self):
        """Test wait_until_ready method"""
        # Start a thread that will set the event after a short delay
        def set_event():
            time.sleep(0.1)
            SecurityServicesInformation._READY_EVENT.set()

        threading.Thread(target=set_event).start()
        
        # This should not block indefinitely
        SecurityServicesInformation.wait_until_ready()
        self.assertTrue(SecurityServicesInformation._READY_EVENT.is_set())

    def test_register_subclass(self):
        """Test subclass registration"""
        class TestSubclass(SecurityServicesInformation):
            pass

        self.assertIn(TestSubclass, SecurityServicesInformation._REGISTRY)

    def test_deregister(self):
        """Test deregister method"""
        class TestSubclass(SecurityServicesInformation):
            pass

        SecurityServicesInformation.deregister(TestSubclass)
        self.assertNotIn(TestSubclass, SecurityServicesInformation._REGISTRY)

    def test_get_registered(self):
        """Test get_registered method"""
        class TestSubclass1(SecurityServicesInformation):
            pass
        class TestSubclass2(SecurityServicesInformation):
            pass

        registered = SecurityServicesInformation.get_registered()
        self.assertEqual(len(registered), 2)
        self.assertIn(TestSubclass1, registered)
        self.assertIn(TestSubclass2, registered)

    @patch('win32evtlog.OpenEventLog')
    @patch('win32evtlog.ReadEventLog')
    def test_security_service_log_finder(self, mock_read_event_log, mock_open_event_log):
        """Test SecurityServiceLogFinder log acquisition"""
        # Mock event log data
        mock_event = MagicMock()
        mock_event.SourceName = "SecurityService"
        mock_event.TimeGenerated.Format.return_value = "2024-01-01"
        mock_event.StringInserts = ["Security alert"]
        
        mock_read_event_log.return_value = [mock_event]
        mock_open_event_log.return_value = MagicMock()

        # Create test security service
        security_service = SecurityService(
            name="TestSecurity",
            status="Running",
            logs=[]
        )

        # Test log acquisition
        SecurityServiceLogFinder.acquire_logs(security_service)
        
        # Verify logs were added
        self.assertTrue(len(security_service.logs) > 0)
        self.assertEqual(security_service.logs[0]["source"], "SecurityService")

    def test_monitor_services(self):
        """Test monitor_services method"""
        # Create a test service
        service = SecurityService(
            name="TestSecurity",
            status="Running",
            logs=[]
        )
        SecurityServicesInformation._SERVICES = [service]

        # Create a log finder instance and test monitoring
        log_finder = SecurityServiceLogFinder()
        with patch('builtins.print') as mock_print:
            log_finder.monitor_services()
            mock_print.assert_called_once()

if __name__ == '__main__':
    unittest.main() 