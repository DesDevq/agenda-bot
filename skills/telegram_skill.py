from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


scheduler = BackgroundScheduler()
scheduler.start()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def enviar_mensaje(tarea: str, chat_id: str):
    bot = Bot(token=TELEGRAM_TOKEN)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(bot.send_message(
            chat_id=chat_id,
            text=f"⏰ Recordatorio: *{tarea}* en 30 minutos!",
            parse_mode="Markdown"
        ))
    finally:
        loop.close()


def programar_mensaje(tarea: str, fecha: str, hora: str, chat_id: str):
    momento = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    recordatorio = momento - timedelta(minutes=30)

    if recordatorio < datetime.now():
        print("⚠️ La hora del recordatorio ya pasó")
        return

    scheduler.add_job(
        func=enviar_mensaje,
        trigger="date",
        run_date=recordatorio,
        args=[tarea, chat_id],
        id=f"recordatorio_{tarea}_{fecha}_{hora}"
    )
    print(f"✅ Recordatorio programado para: {recordatorio}")
