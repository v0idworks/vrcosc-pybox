import psutil
import subprocess

def get_cpu_ram():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return cpu, ram

def get_gpu():
    try:
        out = subprocess.check_output(
            ["nvidia-smi","--query-gpu=utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],encoding="utf-8")
        u, used, total = out.strip().split(", ")
        return int(u), int(used), int(total)
    except:
        return None, None, None
