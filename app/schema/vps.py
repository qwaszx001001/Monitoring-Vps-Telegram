from pydantic import BaseModel
from typing import Optional



class CpuStats(BaseModel):
    cpu_percent: float
    count_cpu: int

class MemoryStats(BaseModel):
    total: int
    available : int
    used: int
    free: int
    cached: Optional[int] = None
    percent: float


