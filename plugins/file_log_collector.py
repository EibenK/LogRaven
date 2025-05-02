from core.registry import Registry


class FileLogCollector(Registry):
    # Pseudo return information for testing purposes.
    def fetch_logs(self): return ["Found 1 file at xyz.xyz",
                                  "Found 2 files at leet.leet"]
