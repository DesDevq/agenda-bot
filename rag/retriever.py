from rag.vector_store import buscar_tareas_similares as _buscar


def buscar_tareas_similares(mensaje: str) -> str:
    return _buscar(mensaje)
