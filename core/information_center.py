import logging
import time
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import List, Any, Dict
from analysis.parser import Parser
from services.agents_information import AgentServicesInformation
from services.security_information import SecurityServicesInformation
from services.system_information import SystemServicesInformation

logger = logging.getLogger(__name__)

class InformationCenter():
    """ Orchestrator/Supervisor class with thread safety """
    def __init__(self):
        # Thread-safe data structures
        self._services_lock = threading.Lock()
        self._services: List[Any] = []
        self._log_queue = Queue()  # Thread-safe queue for logs
        self._running = True
        self._monitoring_lock = threading.Lock()
        self._monitoring_threads: Dict[str, threading.Thread] = {}
        
        # Initialize services with thread safety
        with self._services_lock:
            self._services.extend(AgentServicesInformation.get_registered())
            self._services.extend(SecurityServicesInformation.get_registered())
            self._services.extend(SystemServicesInformation.get_registered())

        self.executor = ThreadPoolExecutor(max_workers=len(self._services))

    def start_monitoring(self):
        """Start monitoring services with thread safety"""
        with self._monitoring_lock:
            for svc in self._services:
                try:
                    instance = svc()
                    instance.wait_until_ready()
                    method = getattr(instance, "monitor_services")
                    
                    # Create a unique thread name for each service
                    thread_name = f"monitor_{instance.__class__.__name__}"
                    
                    # Start monitoring in a separate thread
                    monitor_thread = threading.Thread(
                        target=self._monitor_service,
                        args=(method, instance, thread_name),
                        name=thread_name,
                        daemon=True
                    )
                    
                    self._monitoring_threads[thread_name] = monitor_thread
                    monitor_thread.start()
                    
                except Exception as e:
                    logger.error(f"Error starting monitoring for service {svc.__name__}: {e}")

            # Initialize parser with thread-safe queue
            self.parser = Parser(self._services, self._log_queue)

    def _monitor_service(self, method: callable, instance: Any, thread_name: str):
        """Thread-safe service monitoring with error handling"""
        while self._running:
            try:
                # Get logs from the service
                logs = method()
                
                # Add logs to the queue with service identification
                if logs:
                    self._log_queue.put({
                        'service': instance.__class__.__name__,
                        'logs': logs,
                        'timestamp': time.time()
                    })
                
                time.sleep(20)  # Monitoring interval
                
            except Exception as e:
                logger.error(f"Error in monitoring thread {thread_name}: {e}")
                time.sleep(5)  # Wait before retrying

    def stop(self):
        """Safely stop all monitoring threads"""
        self._running = False
        
        # Wait for all monitoring threads to finish
        with self._monitoring_lock:
            for thread in self._monitoring_threads.values():
                if thread.is_alive():
                    thread.join(timeout=5.0)  # Wait up to 5 seconds for each thread
        
        # Shutdown the thread pool
        self.executor.shutdown(wait=True)
        
        # Clear the log queue
        while not self._log_queue.empty():
            try:
                self._log_queue.get_nowait()
            except:
                pass

    def get_services(self) -> List[Any]:
        """Thread-safe access to services list"""
        with self._services_lock:
            return self._services.copy()  # Return a copy to prevent external modification

    def get_logs(self) -> List[Dict]:
        """Thread-safe access to logs"""
        logs = []
        while not self._log_queue.empty():
            try:
                logs.append(self._log_queue.get_nowait())
            except:
                break
        return logs

