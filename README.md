# 🗓️ Agenda Inteligente — NotiClock Bot

**Repositorio:** https://github.com/DesDevq/agenda-bot

Asistente inteligente de productividad y gestión personal que integra Telegram, Google Calendar y una interfaz web con RAG, multiagentes y MCP.

---

## 📌 Descripción

El sistema permite al usuario enviar mensajes por Telegram para crear eventos y recordatorios en Google Calendar. 30 minutos antes del evento, el bot envía una notificación automática. Además, cuenta con una interfaz web en Streamlit donde se pueden subir documentos y hacer preguntas sobre productividad usando RAG.

---

## 🧠 Arquitectura

- **LLM:** Mistral Large (vía API)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Base vectorial:** ChromaDB (persistente)
- **RAG:** Pipeline completo con chunking por párrafos
- **Multiagentes:** LangGraph con 3 agentes (intérprete, calendario, notificador)
- **MCP:** Servidor FastMCP con tools `crear_recordatorio` y `listar_recordatorios`
- **Skills:** Telegram Skill y Calendar Skill
- **Interfaz:** Streamlit

---

## 📁 Estructura del proyecto

```
agenda-bot/
├── agents/
│   ├── calendar_agent.py
│   ├── interpreter.py
│   └── notifier.py
├── graph/
│   ├── graph.py
│   └── state.py
├── mcp/
│   └── server.py
├── rag/
│   ├── retriever.py
│   └── vector_store.py
├── skills/
│   ├── calendar_skill.py
│   └── telegram_skill.py
├── app.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/DesDevq/agenda-bot.git
cd agenda-bot
```

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales.

### 5. Configurar Google Calendar

Coloca tu archivo `credentials.json` en la raíz del proyecto (obtenido desde Google Cloud Console con la API de Calendar habilitada).

---

## 🚀 Uso

### Bot de Telegram

```bash
python main.py
```

### Interfaz web Streamlit

```bash
streamlit run app.py
```

Ambos procesos deben correr en terminales separadas.

---

## 🔑 Variables de entorno

Ver `.env.example` para la lista completa de variables requeridas:

```
MISTRAL_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

## 📦 Requisitos

- Python 3.11+
- Cuenta de Telegram y bot creado con @BotFather
- Credenciales de Google Cloud con Calendar API habilitada
- API key de Mistral

---

## 👥 Autores

Lizeth Castañeda - proyecto clase Introducción a la Inteligencia Artificial.
