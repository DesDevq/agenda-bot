import os
from skills.calendar_skill import crear_evento_calendar
from graph.state import AgendaState
from dotenv import load_dotenv
load_dotenv()


def crear_evento(state: AgendaState) -> AgendaState:
    print("📅 Agente 2: Creando evento en Google Calendar...")

    try:
        evento_id = crear_evento_calendar(
            tarea=state["tarea"],
            fecha=state["fecha"],
            hora=state["hora"],
            recurrente=state.get("recurrente", False)
        )

        print(f"✅ Evento creado: {evento_id}")
        return {**state,
                "evento_creado": True,
                "evento_id":     evento_id}

    except Exception as e:
        print(f"❌ Error creando evento: {e}")
        return {**state,
                "evento_creado": False,
                "error":         str(e)}
