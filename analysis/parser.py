import logging

logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, services):
        self.services = services
        self.filter_logs()

    def filter_logs(self):
        for service in self.services:
            if isinstance(type(object), service):
                print(service.Name, "\n")

if __name__ == "__main__":
    p = Parser([])
    
    

