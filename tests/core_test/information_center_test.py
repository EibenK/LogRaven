import unittest
from unittest.mock import Mock, patch
import time

from core.information_center import InformationCenter
from services.agents_information import AgentServicesInformation
from services.security_information import SecurityServicesInformation
from services.system_information import SystemServicesInformation

class TestInformationCenter(unittest.TestCase):
    def setUp(self):
        self.info_center = InformationCenter()

    def test_initialization(self):
        """Test if InformationCenter initializes correctly with all services"""
        self.assertIsNotNone(self.info_center.services)
        self.assertTrue(len(self.info_center.services) > 0)
        self.assertTrue(self.info_center.running)
        self.assertIsNotNone(self.info_center.executor)

    def test_get_services(self):
        """Test if get_services returns the correct list of services"""
        services = self.info_center.get_services()
        self.assertEqual(services, self.info_center.services)

    @patch('time.sleep')
    def test_wrap_func(self, mock_sleep):
        """Test if _wrap_func executes the given function and sleeps"""
        mock_func = Mock()
        self.info_center.running = True
        self.info_center._wrap_func(mock_func, 20)
        mock_func.assert_called_once()
        mock_sleep.assert_called_once_with(20)

    def test_stop(self):
        """Test if stop method correctly stops the monitoring"""
        self.info_center.stop()
        self.assertFalse(self.info_center.running)
        self.assertTrue(self.info_center.executor._shutdown)

    @patch('concurrent.futures.ThreadPoolExecutor.submit')
    def test_start_monitoring(self, mock_submit):
        """Test if start_monitoring submits tasks to the executor"""
        # Mock the service classes
        mock_service = Mock()
        mock_service.wait_until_ready = Mock()
        mock_service.monitor_services = Mock()
        
        # Replace services with our mock
        self.info_center.services = [mock_service]
        
        # Start monitoring
        self.info_center.start_monitoring()
        
        # Verify the service was initialized and task was submitted
        mock_service.wait_until_ready.assert_called_once()
        mock_submit.assert_called_once()

if __name__ == '__main__':
    unittest.main() 