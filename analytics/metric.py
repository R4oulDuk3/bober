import psutil
prefix = "bobst_pi"

def format_metric_name(name):
    return prefix + "_" + name

class Metric:
    def __init__(self, name: str, value: float, metric_type: str):
        self.value = value
        self.type = metric_type
        self.name = format_metric_name(name)

    @staticmethod
    def gauge(name: str, value: float) -> 'Metric':
        return Metric(name, value, "gauge")


    @staticmethod
    def counter(name: str, value: float) -> 'Metric':
        return Metric(name, value, "counter")


class MetricsRegistry:
    def __init__(self):
        self.metrics = {}


    def inc_counter(self, name: str, value: float):
        if format_metric_name(name) not in self.metrics:
            self.metrics[format_metric_name(name)] = Metric.counter(name, 0)

        self.metrics[format_metric_name(name)].value += value

    def inc_gauge(self, name: str, value: float):
        if format_metric_name(name) not in self.metrics:
            self.metrics[format_metric_name(name)] = Metric.gauge(name, value)

        self.metrics[format_metric_name(name)].value = value

    def get_metrics(self) -> list:
        return [
            {
                'name': metric.name,
                'type': metric.type,
                'value': metric.value
            }
            for metric in self.metrics.values()
        ]

    def observe_system_metrics(self):
        """
        Observes various system metrics and records them as gauges
        """
        # CPU Metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self.inc_gauge("cpu_usage_percent", cpu_percent)

        # CPU Frequency
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            self.inc_gauge("cpu_freq_current", cpu_freq.current)
            if hasattr(cpu_freq, 'min'):
                self.inc_gauge("cpu_freq_min", cpu_freq.min)
            if hasattr(cpu_freq, 'max'):
                self.inc_gauge("cpu_freq_max", cpu_freq.max)

        # Memory Metrics
        mem = psutil.virtual_memory()
        self.inc_gauge("memory_total_gb", round(mem.total / (1024 ** 3), 2))
        self.inc_gauge("memory_available_gb", round(mem.available / (1024 ** 3), 2))
        self.inc_gauge("memory_used_gb", round(mem.used / (1024 ** 3), 2))
        self.inc_gauge("memory_percent", mem.percent)

        # Disk Metrics
        disk = psutil.disk_usage('/')
        self.inc_gauge("disk_total_gb", round(disk.total / (1024 ** 3), 2))
        self.inc_gauge("disk_used_gb", round(disk.used / (1024 ** 3), 2))
        self.inc_gauge("disk_free_gb", round(disk.free / (1024 ** 3), 2))
        self.inc_gauge("disk_percent", disk.percent)

        # Load Average (1, 5, 15 minutes)
        try:
            load1, load5, load15 = psutil.getloadavg()
            self.inc_gauge("load_1min", load1)
            self.inc_gauge("load_5min", load5)
            self.inc_gauge("load_15min", load15)
        except (AttributeError, OSError):
            # Might not be available on some systems
            pass

        # Temperature (if available)
        try:
            temperatures = psutil.sensors_temperatures()
            if temperatures:
                for name, entries in temperatures.items():
                    for idx, entry in enumerate(entries):
                        self.inc_gauge(f"temperature_{name}_{idx}", entry.current)
        except (AttributeError, OSError):
            # Might not be available on some systems
            pass

        # Network IO Counters
        net_io = psutil.net_io_counters()
        self.inc_gauge("network_bytes_sent", net_io.bytes_sent)
        self.inc_gauge("network_bytes_recv", net_io.bytes_recv)


if __name__ == "__main__":
    try:
        # Initialize registry
        registry = MetricsRegistry()

        print("Starting system metrics collection...")
        print("Press Ctrl+C to stop\n")

        # Continuous monitoring loop
        while True:
            registry.observe_system_metrics()
            metrics = registry.get_metrics()

            # Clear screen (optional - comment out if you don't want this)
            print("\033[H\033[J")  # Clear screen

            # Print current timestamp
            from datetime import datetime

            print(f"=== System Metrics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

            # Print metrics in a formatted way
            for metric in sorted(metrics, key=lambda x: x['name']):
                print(f"{metric['name']}:")
                print(f"  Type: {metric['type']}")
                print(f"  Value: {metric['value']}")
                print()

            # Wait before next collection
            import time

            time.sleep(5)  # Update every 5 seconds

    except KeyboardInterrupt:
        print("\nStopping metrics collection...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("Metrics collection ended")