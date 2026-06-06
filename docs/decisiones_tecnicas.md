# Decisiones Técnicas — Agenda Inteligente

---

## Decisión 1: Mistral como LLM principal

**Contexto:**
El proyecto requería un LLM capaz de interpretar mensajes en lenguaje natural para extraer tareas, fechas y horas, además de responder preguntas sobre productividad basándose en documentos indexados.

**Decisión:**
Se eligió Mistral Large vía API como modelo principal del sistema.

**Consecuencias:**

- Permite acceso gratuito o de bajo costo sin necesidad de ejecutar un modelo local.
- Ofrece buena comprensión del español, lo cual es clave para interpretar correctamente los mensajes del usuario.
- Depende de conexión a internet y disponibilidad de la API externa.
- Alternativas como Llama 3.2 local fueron descartadas por requerir hardware dedicado.

---

## Decisión 2: Chunking por párrafos en lugar de caracteres fijos

**Contexto:**
El pipeline RAG inicial dividía los documentos en fragmentos de 500 caracteres fijos, lo que frecuentemente cortaba ideas a la mitad y reducía la calidad de las respuestas del asistente.

**Decisión:**
Se implementó un chunking semántico basado en párrafos (separador `\n\n`), con un límite máximo de 600 caracteres por chunk. Los párrafos más largos se subdividen por oraciones.

**Consecuencias:**

- Cada chunk contiene una idea completa, mejorando la coherencia del contexto enviado al LLM.
- Las respuestas del asistente son más precisas y relevantes.
- El número de chunks varía por documento, pero ChromaDB lo maneja eficientemente con upsert.
- Ligero aumento en tiempo de procesamiento al indexar documentos grandes.

---

## Decisión 3: ChromaDB como base vectorial persistente

**Contexto:**
El sistema necesitaba almacenar embeddings de documentos y tareas de forma que sobrevivieran entre sesiones, sin depender de servicios externos ni infraestructura compleja.

**Decisión:**
Se eligió ChromaDB con `PersistentClient` apuntando a una carpeta local `./chroma_db`, con dos colecciones separadas: `tareas_usuario` y `documentos_usuario`.

**Consecuencias:**

- Los datos persisten en disco entre reinicios del sistema sin configuración adicional.
- La separación en dos colecciones evita mezclar el contexto de tareas del bot con el contenido de documentos subidos.
- Es completamente gratuito y open source, sin límites de uso.
- No es adecuado para producción a escala, pero es suficiente para el alcance del proyecto universitario.
