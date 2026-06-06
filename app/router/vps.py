
from fastapi import APIRouter
try:
    from app.service.vps import get_cpu_stats, get_memory_stats
except ModuleNotFoundError:
    from service.vps import get_cpu_stats, get_memory_stats


router = APIRouter(tags=["vps"])

@router.get("/cpu")
def cpu():
    return get_cpu_stats()


@router.get("/memory")
def memory():
    return get_memory_stats()
   
