# monitor/system_checker.py
import psutil

def snapshot():
    """
    Take a snapshot of current system usage (CPU, Memory, Disk).
    Returns:
        tuple: (cpu_percent, mem_percent, disk_percent)
    """
    # cpu_percent with interval=0.5 for a small smoothing without blocking too long
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return cpu, mem, disk