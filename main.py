from aggregation.log_aggregator import LogAggregator

# Dynamically using SecurityLogCollector and SystemLogCollector through
# inheritance and abstraction within log_aggregation.
from aggregation.sec_log_collector import SecurityLogCollector
from aggregation.sys_log_collector import SystemLogCollector


class Main:
    def __init__(self):
        data = LogAggregator.get_parsed_logs()
        print(data)


if __name__ == "__main__":
    app = Main()
