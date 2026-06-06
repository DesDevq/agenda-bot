import socket
from graph.graph import crear_grafo
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


grafo = crear_grafo()

old_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]


socket.getaddrinfo = new_getaddrinfo


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text
    chat_id = str(update.effective_chat.id)

    await update.message.reply_text("🤖 Procesando tu solicitud...")

    try:
        resultado = grafo.invoke({
            "mensaje_usuario": mensaje,
            "chat_id": chat_id
        })

        if resultado.get("error"):
            await update.message.reply_text(f"❌ Error: {resultado['error']}")
        else:
            await update.message.reply_text(
                resultado.get("respuesta", "✅ Listo!"),
                parse_mode="Markdown"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Ocurrió un error: {str(e)}")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("🤖 Bot iniciado. Esperando mensajes en Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()
