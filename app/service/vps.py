import psutil
from schema.vps import CpuStats, MemoryStats



def get_cpu_stats() -> CpuStats:
    """
    GetCPU stats
    """
    return CpuStats(
        cpu_percent=psutil.cpu_percent(1),
        count_cpu=psutil.cpu_count(logical=True)
    )


def get_memory_stats() -> MemoryStats:
    memory = psutil.virtual_memory()
    print(memory)

    gb, mb = divmod(int(memory.total), 1024**3)
    print(memory.total)
    print(gb, mb)
    available_gb, available_mb = divmod(int(memory.available), 1024**3)
    used_gb, used_mb = divmod(int(memory.used), 1024**3)
    free_gb, free_mb = divmod(int(memory.free), 1024**3)

    percent = memory.percent

    return MemoryStats(
        total=gb,
        available=available_gb,
        used=used_gb,
        free=free_gb,
        percent=percent,
    )
