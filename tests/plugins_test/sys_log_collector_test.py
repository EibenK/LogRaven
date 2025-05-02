import unittest
from plugins.sys_log_collector import SystemLogCollector

class SysLogCollectorTest(unittest.TestCase):
    

    def test_fetch_logs(self):
        sys_logs = SystemLogCollector()
        self.assertIsInstance(sys_logs.fetch_logs(), list)
    
if __name__ == "__main__":
    unittest.main()

