import os
from skills.telegram_skill import programar_mensaje
from graph.state import AgendaState
from dotenv import load_dotenv
load_dotenv()


def programar_recordatorio(state: AgendaState) -> AgendaState:
    print("🔔 Agente 3: Programando recordatorio en Telegram...")

    if not state.get("evento_creado"):
        return {**state,
                "recordatorio_programado": False,
                "error": "No se pudo crear el evento"}

    try:
        programar_mensaje(
            tarea=state["tarea"],
            fecha=state["fecha"],
            hora=state["hora"],
            chat_id=state["chat_id"]
        )

        respuesta_final = (
            f"✅ {state['respuesta']}\n\n"
            f"📅 Evento creado en Google Calendar\n"
            f"🔔 Te recordaré 30 minutos antes por Telegram"
        )

        print(f"✅ Recordatorio programado")
        return {**state,
                "recordatorio_programado": True,
                "respuesta": respuesta_final}

    except Exception as e:
        print(f"❌ Error programando recordatorio: {e}")
        return {**state,
                "recordatorio_programado": False,
                "error": str(e)}
