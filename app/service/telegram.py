import asyncio
import datetime
from sys import stdout
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
import telegram 
import os
from dotenv import load_dotenv
import logging
from service.vps import get_cpu_stats, get_memory_stats

logger = logging.getLogger(__name__)
load_dotenv()




async def send_message(chat_id:str , text:str):
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable not set")
    bot = telegram.Bot(token=TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)
    logger.info(f"Kirim pesan ke chat {chat_id}: {text}")
    return True
    

async def command(chat_id: str , cmd: str, user: str):
    """
    Handle command
    """

    if cmd == "/cpu":
        await send_message(chat_id, get_cpu_stats())
    if cmd == "/memory":
        await send_message(chat_id, get_memory_stats())
    else:
        await send_message(chat_id, "Unknown command")

async def alert():
    """
    Send alert message to chat
    """
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    while True:
        try:
            cpu = get_cpu_stats()
            memory = get_memory_stats()

            if cpu.cpu_percent > 80:
                await send_message(CHAT_ID, f"Alert: CPU terpakai = {cpu.cpu_percent}%")
            if memory.percent > 60:
                await send_message(CHAT_ID, f"Alert: Memory terpakai = {memory.percent}%")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in alert: {e}")
            await asyncio.sleep(1)

        await asyncio.sleep(60)



async def logs():
    """
    Send logs message to chat
    """
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID environment variable not set")
    STATUS = {403,502,404}
    counter = defaultdict(int)
    start_time = datetime.now()
    process = await asyncio.create_subprocess_exec(
        ["tail","-f","/var/log/caddy/access.log"],
        stdout = subprocess.PIPE,
        text = True,
    )

    while True:
        lin = await process.stdout.readline()
        try:
            log = json.loads(lin)
            status = log.get("status")
            if status not in STATUS:
                continue
            path = log.get(f"request",{}).get("uri","/")
            counter[(status,path)] += 1
        except Exception as e:
            continue

        if datetime.now() - start_time > timedelta(hours=1):
            logger.info("=" * 50)
            logger.info("REPORT 1 JAM")
            logger.info("=" * 50)

            hasil = sorted(counter.items(), key=lambda x: x[1], reverse=True)

            for (status, path), total in hasil:
                logger.info(f"{status} | {total:5d} | {path}")


            await send_message(CHAT_ID, f"REPORT 1 JAM\n{report}")
            counter.clear()
            start_time = datetime.now()




    

