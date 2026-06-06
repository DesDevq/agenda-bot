from typing import TypedDict, Optional, List


class AgendaState(TypedDict):
    # Input del usuario
    mensaje_usuario:    str
    chat_id:            str

    # Agente 1 - Interpretador
    tarea:              Optional[str]
    fecha:              Optional[str]
    hora:               Optional[str]
    recurrente:         Optional[bool]

    # Agente 2 - Calendario
    evento_creado:      Optional[bool]
    evento_id:          Optional[str]

    # Agente 3 - Notificador
    recordatorio_programado: Optional[bool]

    # Control
    respuesta:          Optional[str]
    error:              Optional[str]
