import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import re
import threading
from queue import Queue

logger = logging.getLogger(__name__)

class LogEntry:
    def __init__(self, source: str, timestamp: str, message: List[str], service_type: str):
        self.source = source
        self.timestamp = timestamp
        self.message = message
        self.service_type = service_type
        self.severity = self._determine_severity()
        self.categories = self._categorize_log()

    def _determine_severity(self) -> str:
        """Determine the severity level of the log entry based on keywords."""
        message_text = ' '.join(self.message).lower()
        
        # Define severity patterns
        severity_patterns = {
            'critical': r'critical|fatal|severe|emergency',
            'error': r'error|failed|failure|exception',
            'warning': r'warning|warn|caution|attention',
            'info': r'info|information|notice',
            'debug': r'debug|trace'
        }

        for severity, pattern in severity_patterns.items():
            if re.search(pattern, message_text):
                return severity
        return 'unknown'

    def _categorize_log(self) -> List[str]:
        """Categorize the log entry based on its content."""
        categories = []
        message_text = ' '.join(self.message).lower()

        # Define category patterns
        category_patterns = {
            'security': r'security|auth|login|permission|access|firewall|antivirus',
            'performance': r'performance|slow|timeout|latency|response time',
            'system': r'system|service|process|thread|memory|cpu|disk',
            'network': r'network|connection|socket|port|ip|dns|http',
            'database': r'database|sql|query|transaction|connection pool',
            'application': r'application|app|module|feature|function'
        }

        for category, pattern in category_patterns.items():
            if re.search(pattern, message_text):
                categories.append(category)

        return categories if categories else ['general']

    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary format."""
        return {
            'source': self.source,
            'timestamp': self.timestamp,
            'message': self.message,
            'service_type': self.service_type,
            'severity': self.severity,
            'categories': self.categories
        }

class Parser:
    def __init__(self, services: List[Any], log_queue: Queue):
        self.services = services
        self.log_queue = log_queue
        self.parsed_logs: List[LogEntry] = []
        self._logs_lock = threading.Lock()
        self._processing_thread = threading.Thread(target=self._process_logs, daemon=True)
        self._processing_thread.start()

    def _process_logs(self):
        """Continuously process logs from the queue in a thread-safe manner."""
        while True:
            try:
                # Get log entry from queue
                log_data = self.log_queue.get()
                
                # Process the log entry
                if isinstance(log_data, dict):
                    service_type = log_data.get('service', 'unknown')
                    logs = log_data.get('logs', [])
                    
                    for log in logs:
                        if isinstance(log, dict):
                            try:
                                log_entry = LogEntry(
                                    source=log.get('source', 'unknown'),
                                    timestamp=log.get('timestamp', ''),
                                    message=log.get('message', []),
                                    service_type=service_type
                                )
                                
                                # Thread-safe addition to parsed_logs
                                with self._logs_lock:
                                    self.parsed_logs.append(log_entry)
                                    
                            except Exception as e:
                                logger.error(f"Error parsing log entry: {e}")
                
            except Exception as e:
                logger.error(f"Error processing logs: {e}")

    def get_logs_by_severity(self, severity: str) -> List[LogEntry]:
        """Thread-safe access to logs by severity."""
        with self._logs_lock:
            return [log for log in self.parsed_logs if log.severity == severity]

    def get_logs_by_category(self, category: str) -> List[LogEntry]:
        """Thread-safe access to logs by category."""
        with self._logs_lock:
            return [log for log in self.parsed_logs if category in log.categories]

    def get_logs_by_service_type(self, service_type: str) -> List[LogEntry]:
        """Thread-safe access to logs by service type."""
        with self._logs_lock:
            return [log for log in self.parsed_logs if log.service_type == service_type]

    def get_logs_by_time_range(self, start_time: str, end_time: str) -> List[LogEntry]:
        """Thread-safe access to logs within a time range."""
        try:
            start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            
            with self._logs_lock:
                return [
                    log for log in self.parsed_logs
                    if start <= datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S") <= end
                ]
        except ValueError as e:
            logger.error(f"Invalid time format: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Thread-safe access to log statistics."""
        with self._logs_lock:
            stats = {
                'total_logs': len(self.parsed_logs),
                'severity_distribution': {},
                'category_distribution': {},
                'service_type_distribution': {}
            }

            for log in self.parsed_logs:
                # Count severity distribution
                stats['severity_distribution'][log.severity] = \
                    stats['severity_distribution'].get(log.severity, 0) + 1

                # Count category distribution
                for category in log.categories:
                    stats['category_distribution'][category] = \
                        stats['category_distribution'].get(category, 0) + 1

                # Count service type distribution
                stats['service_type_distribution'][log.service_type] = \
                    stats['service_type_distribution'].get(log.service_type, 0) + 1

            return stats

if __name__ == "__main__":
    # Example usage
    p = Parser([])
    # Add test data and demonstrate functionality
    
    

