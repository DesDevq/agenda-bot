import os
import json
from graph.state import AgendaState
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv()


client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def interpretar_mensaje(state: AgendaState) -> AgendaState:
    print("🧠 Agente 1: Interpretando mensaje...")

    from rag.retriever import buscar_tareas_similares
    contexto_rag = buscar_tareas_similares(state["mensaje_usuario"])

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": f"""Eres un asistente que interpreta mensajes en lenguaje natural 
para crear recordatorios y eventos en el calendario.

MENSAJE DEL USUARIO:
{state["mensaje_usuario"]}

TAREAS FRECUENTES DEL USUARIO (referencia):
{contexto_rag}

Extrae la información del mensaje y responde SOLO en JSON:
{{
    "tarea": "descripción clara de la tarea o recordatorio",
    "fecha": "YYYY-MM-DD (fecha del evento, usa la fecha más lógica)",
    "hora": "HH:MM (hora en formato 24h)",
    "recurrente": false,
    "frecuencia": "none/daily/weekly/monthly",
    "respuesta": "mensaje amigable confirmando lo que entendiste en español"
}}

Si el usuario dice 'todos los lunes' recurrente es true y frecuencia es weekly.
Si no menciona año asume 2026. El año actual es 2026.
Si no menciona hora asume 09:00."""
        }]
    )

    texto = response.choices[0].message.content.strip()
    if "```" in texto:
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]

    resultado = json.loads(texto.strip())

    from rag.vector_store import guardar_tarea
    guardar_tarea(state["mensaje_usuario"], resultado["tarea"])

    print(f"✅ Tarea: {resultado['tarea']}")
    print(f"✅ Fecha: {resultado['fecha']} {resultado['hora']}")

    return {**state,
            "tarea":      resultado["tarea"],
            "fecha":      resultado["fecha"],
            "hora":       resultado["hora"],
            "recurrente": resultado["recurrente"],
            "respuesta":  resultado["respuesta"]}
