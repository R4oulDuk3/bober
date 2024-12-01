import platform
import psutil
import os


def get_system_info():
    """
    Get detailed system information from Raspberry Pi
    Returns a dictionary containing system information
    """
    system_info = {
        # Python Version
        'pythonVersion': platform.python_version(),
        # OS Information
        'osName': os.name,
        'osSystem': platform.system(),
        'osRelease': platform.release(),
        'osVersion': platform.version(),
        # CPU Information
        'cpuCountPhysical': psutil.cpu_count(logical=False),
        'cpuCountLogical': psutil.cpu_count(logical=True),
        'cpuFreqCurrent': psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else 'N/A',
        # Memory Information
        'totalRam': round(psutil.virtual_memory().total / (1024 ** 3), 2),  # GB
        # Disk Information
        'diskTotal': round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # GB
    }
    return system_info


def get_system_info_string():
    """
    Returns formatted system information as a string
    """
    info = get_system_info()

    return f"""

Python Version: {info['python_version']}

OS Information:
OS Name: {info['os_name']}
System: {info['os_system']}
Release: {info['os_release']}
Version: {info['os_version']}

CPU Information:
Physical CPU cores: {info['cpu_count_physical']}
Logical CPU cores: {info['cpu_count_logical']}
CPU Frequency: {info['cpu_freq_current']} MHz

Memory Information:
Total RAM: {info['total_ram']} GB

Disk Information:
Total Disk Space: {info['disk_total']} GB"""


if __name__ == "__main__":
    print(get_system_info_string())