import os
from skills.telegram_skill import programar_mensaje
from skills.calendar_skill import crear_evento_calendar
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()


mcp = FastMCP("agenda-bot")


@mcp.tool()
def crear_recordatorio(
    tarea: str,
    fecha: str,
    hora: str,
    recurrente: bool = False
) -> str:
    """
    Crea un evento en Google Calendar y programa
    un recordatorio en Telegram 30 minutos antes.

    Args:
        tarea: descripción de la tarea o recordatorio
        fecha: fecha en formato YYYY-MM-DD
        hora: hora en formato HH:MM
        recurrente: si el evento se repite semanalmente

    Returns:
        Confirmación del evento creado
    """
    evento_id = crear_evento_calendar(
        tarea=tarea,
        fecha=fecha,
        hora=hora,
        recurrente=recurrente
    )

    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    programar_mensaje(
        tarea=tarea,
        fecha=fecha,
        hora=hora,
        chat_id=chat_id
    )

    return f"✅ Evento '{tarea}' creado para {fecha} a las {hora}"


@mcp.tool()
def listar_recordatorios() -> str:
    """
    Lista los recordatorios programados pendientes.
    """
    from skills.telegram_skill import scheduler
    jobs = scheduler.get_jobs()

    if not jobs:
        return "No hay recordatorios programados."

    lista = "\n".join([f"- {job.id}" for job in jobs])
    return f"Recordatorios pendientes:\n{lista}"


if __name__ == "__main__":
    mcp.run()
