import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time

from services.agents_information import AgentServicesInformation, AgentService, AgentServiceLogFinder

class TestAgentServicesInformation(unittest.TestCase):
    def setUp(self):
        # Reset the class variables before each test
        AgentServicesInformation._REGISTRY = []
        AgentServicesInformation._SERVICES = []
        AgentServicesInformation._READY_EVENT = threading.Event()
        AgentServicesInformation._INIT_DONE = False

    def test_agent_service_dataclass(self):
        """Test AgentService dataclass initialization"""
        service = AgentService(
            name="TestAgent",
            status="Running",
            logs=[]
        )
        self.assertEqual(service.name, "TestAgent")
        self.assertEqual(service.status, "Running")
        self.assertEqual(service.logs, [])

    @patch('wmi.WMI')
    def test_initialization(self, mock_wmi):
        """Test if AgentServicesInformation initializes correctly"""
        # Mock WMI service
        mock_service = MagicMock()
        mock_service.DisplayName = "Test Agent Service"
        mock_service.Name = "TestAgent"
        mock_service.State = "Running"
        mock_wmi.return_value.Win32_Service.return_value = [mock_service]

        # Initialize the class
        agent_info = AgentServicesInformation()
        
        # Verify initialization
        self.assertTrue(AgentServicesInformation._INIT_DONE)
        self.assertTrue(AgentServicesInformation._READY_EVENT.is_set())
        self.assertEqual(len(AgentServicesInformation._SERVICES), 1)

    def test_wait_until_ready(self):
        """Test wait_until_ready method"""
        # Start a thread that will set the event after a short delay
        def set_event():
            time.sleep(0.1)
            AgentServicesInformation._READY_EVENT.set()

        threading.Thread(target=set_event).start()
        
        # This should not block indefinitely
        AgentServicesInformation.wait_until_ready()
        self.assertTrue(AgentServicesInformation._READY_EVENT.is_set())

    def test_register_subclass(self):
        """Test subclass registration"""
        class TestSubclass(AgentServicesInformation):
            pass

        self.assertIn(TestSubclass, AgentServicesInformation._REGISTRY)

    def test_deregister(self):
        """Test deregister method"""
        class TestSubclass(AgentServicesInformation):
            pass

        AgentServicesInformation.deregister(TestSubclass)
        self.assertNotIn(TestSubclass, AgentServicesInformation._REGISTRY)

    def test_get_registered(self):
        """Test get_registered method"""
        class TestSubclass1(AgentServicesInformation):
            pass
        class TestSubclass2(AgentServicesInformation):
            pass

        registered = AgentServicesInformation.get_registered()
        self.assertEqual(len(registered), 2)
        self.assertIn(TestSubclass1, registered)
        self.assertIn(TestSubclass2, registered)

    @patch('win32evtlog.OpenEventLog')
    @patch('win32evtlog.ReadEventLog')
    def test_agent_service_log_finder(self, mock_read_event_log, mock_open_event_log):
        """Test AgentServiceLogFinder log acquisition"""
        # Mock event log data
        mock_event = MagicMock()
        mock_event.SourceName = "TestAgent"
        mock_event.TimeGenerated.Format.return_value = "2024-01-01"
        mock_event.StringInserts = ["Test message"]
        
        mock_read_event_log.return_value = [mock_event]
        mock_open_event_log.return_value = MagicMock()

        # Create test agent
        agent = AgentService(
            name="TestAgent",
            status="Running",
            logs=[]
        )

        # Test log acquisition
        AgentServiceLogFinder.acquire_logs(agent)
        
        # Verify logs were added
        self.assertTrue(len(agent.logs) > 0)
        self.assertEqual(agent.logs[0]["source"], "TestAgent")

if __name__ == '__main__':
    unittest.main() 