import psutil
from datetime import datetime

def main():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    print(f"[{ts}] CPU: {cpu}% | RAM: {mem}% | DISK: {disk}%")

if __name__ == "__main__":
    main()
