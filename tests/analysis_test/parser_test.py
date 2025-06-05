import unittest
from queue import Queue
import time
from analysis.parser import Parser, LogEntry

class TestParser(unittest.TestCase):
    def setUp(self):
        self.log_queue = Queue()
        self.parser = Parser([], self.log_queue)

    def test_log_processing(self):
        # Create test log data
        test_log = {
            'service': 'AgentService',
            'logs': [{
                'source': 'TestAgent',
                'timestamp': '2024-01-01 10:00:00',
                'message': ['Critical security alert: Unauthorized access attempt']
            }],
            'timestamp': time.time()
        }

        # Add log to queue
        self.log_queue.put(test_log)

        # Wait for processing
        time.sleep(1)

        # Check if log was processed
        critical_logs = self.parser.get_logs_by_severity('critical')
        self.assertEqual(len(critical_logs), 1)
        self.assertEqual(critical_logs[0].source, 'TestAgent')
        self.assertEqual(critical_logs[0].severity, 'critical')
        self.assertIn('security', critical_logs[0].categories)

    def test_multiple_logs(self):
        # Create multiple test logs
        test_logs = [
            {
                'service': 'SecurityService',
                'logs': [{
                    'source': 'SecurityMonitor',
                    'timestamp': '2024-01-01 10:00:00',
                    'message': ['Warning: Suspicious activity detected']
                }],
                'timestamp': time.time()
            },
            {
                'service': 'SystemService',
                'logs': [{
                    'source': 'SystemMonitor',
                    'timestamp': '2024-01-01 10:01:00',
                    'message': ['Info: System check completed']
                }],
                'timestamp': time.time()
            }
        ]

        # Add logs to queue
        for log in test_logs:
            self.log_queue.put(log)

        # Wait for processing
        time.sleep(1)

        # Check statistics
        stats = self.parser.get_statistics()
        self.assertEqual(stats['total_logs'], 2)
        self.assertEqual(stats['severity_distribution']['warning'], 1)
        self.assertEqual(stats['severity_distribution']['info'], 1)

    def test_time_range_filtering(self):
        # Create test logs with different timestamps
        test_logs = [
            {
                'service': 'TestService',
                'logs': [
                    {
                        'source': 'TestSource1',
                        'timestamp': '2024-01-01 10:00:00',
                        'message': ['Test message 1']
                    },
                    {
                        'source': 'TestSource2',
                        'timestamp': '2024-01-01 11:00:00',
                        'message': ['Test message 2']
                    }
                ],
                'timestamp': time.time()
            }
        ]

        # Add logs to queue
        for log in test_logs:
            self.log_queue.put(log)

        # Wait for processing
        time.sleep(1)

        # Test time range filtering
        filtered_logs = self.parser.get_logs_by_time_range(
            '2024-01-01 09:00:00',
            '2024-01-01 10:30:00'
        )
        self.assertEqual(len(filtered_logs), 1)
        self.assertEqual(filtered_logs[0].source, 'TestSource1')

if __name__ == '__main__':
    unittest.main() 