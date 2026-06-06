from langgraph.graph import StateGraph, END
from graph.state import AgendaState
from agents.interpreter import interpretar_mensaje
from agents.calendar_agent import crear_evento
from agents.notifier import programar_recordatorio


def crear_grafo():
    graph = StateGraph(AgendaState)

    # Nodos
    graph.add_node("interpretar",  interpretar_mensaje)
    graph.add_node("calendario",   crear_evento)
    graph.add_node("notificador",  programar_recordatorio)

    # Flujo
    graph.set_entry_point("interpretar")
    graph.add_edge("interpretar", "calendario")
    graph.add_edge("calendario",  "notificador")
    graph.add_edge("notificador", END)

    return graph.compile()
