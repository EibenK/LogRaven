from core.registry import Registry


class SystemLogCollector(Registry):
    # Pseudo return information for testing purposes.
    def fetch_logs(self): return ["Login Successful",
                                  "System Performance Check - Healthy"]
