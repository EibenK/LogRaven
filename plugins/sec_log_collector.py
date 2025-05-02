from core.registry import Registry


class SecurityLogCollector(Registry):
    # Pseudo return information for testing purposes.
    def fetch_logs(self): return ["Kernel Error detected",
                                  "Running application x.x"]

