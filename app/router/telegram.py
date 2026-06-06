
from fastapi import APIRouter, Request
from service.telegram import send_message, command, get_cpu_stats, get_memory_stats

import telegram



router = APIRouter(prefix="/api", tags=["telegram"])



@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()


    if data["message"]["text"] == "/start":
        await send_message(chat_id=data["message"]["chat"]["id"], text="Hello, I'm a bot!")
    if data["message"]["text"] == "/cpu":
        cpu = get_cpu_stats()
        print(cpu.cpu_percent)
        print(cpu.count_cpu)
        await send_message(chat_id=data["message"]["chat"]["id"], text=f"CPU terpakai = {cpu.cpu_percent}% \n Jumlah CPU = {cpu.count_cpu}")
    if data["message"]["text"] == "/memory":
        memory = get_memory_stats()
        print(memory.total)
        await send_message(chat_id=data["message"]["chat"]["id"], text=f"Total Memory = {memory.total}GB \n Available Memory = {memory.available}GB \n Used Memory = {memory.used}GB \n Free Memory = {memory.free}GB")
    return {"ok": True}
