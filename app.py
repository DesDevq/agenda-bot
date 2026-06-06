from dotenv import load_dotenv
import streamlit as st
import io
import os
from mistralai import Mistral
from rag.vector_store import (
    guardar_tarea,
    buscar_tareas_similares,
    guardar_documento,
    buscar_en_documentos
)
import socket
old_getaddrinfo = socket.getaddrinfo


def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]


socket.getaddrinfo = new_getaddrinfo


load_dotenv()

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None


mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def consultar_asistente(pregunta: str) -> str:
    contexto_tareas = buscar_tareas_similares(pregunta)
    contexto_docs = buscar_en_documentos(pregunta)

    response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": f"""Eres un asistente de productividad y gestión.

Tareas registradas del usuario:
{contexto_tareas}

Información de documentos subidos:
{contexto_docs}

Pregunta: {pregunta}
Responde en español de forma clara y concisa."""}]
    )
    return response.choices[0].message.content


def leer_archivo(f) -> str:
    ext = f.name.lower().split(".")[-1]
    b = f.getvalue()
    if ext == "txt":
        try:
            return b.decode("utf-8")
        except Exception:
            return b.decode("latin-1", errors="ignore")
    if ext == "pdf":
        if PdfReader is None:
            raise RuntimeError("Instala PyPDF2: pip install PyPDF2")
        r = PdfReader(io.BytesIO(b))
        return "\n".join(p.extract_text() or "" for p in r.pages).strip()
    raise ValueError("Solo .txt o .pdf")


# ── UI ───────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Agenda IA", page_icon="🗓️")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "documentos" not in st.session_state:
    st.session_state.documentos = []

st.title("🗓️ Agenda Inteligente")
st.divider()

# ── Subir documentos ─────────────────────────────────────────────────────────
st.subheader("📄 Subir documentos")
st.caption("Sube archivos .txt o .pdf")

archivos = st.file_uploader(
    "Sube archivos .txt o .pdf",
    type=["txt", "pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if archivos:
    for arch in archivos:
        doc_id = f"{arch.name}-{arch.size}"
        if not any(d["id"] == doc_id for d in st.session_state.documentos):
            try:
                contenido = leer_archivo(arch)
                st.session_state.documentos.append({
                    "id": doc_id,
                    "nombre": arch.name,
                    "contenido": contenido,
                    "indexado": False
                })
            except Exception as e:
                st.error(str(e))

if st.session_state.documentos:
    for doc in st.session_state.documentos:
        col1, col2 = st.columns([4, 1])
        with col1:
            estado = "✅ Indexado" if doc["indexado"] else "⏳ Pendiente"
            st.write(f"📄 {doc['nombre']} — {estado}")
        with col2:
            if not doc["indexado"]:
                if st.button("Indexar", key=f"idx_{doc['id']}"):
                    try:
                        guardar_documento(doc["nombre"], doc["contenido"])
                        doc["indexado"] = True
                        st.success("✅ Documento indexado")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

st.divider()

# ── Asistente ────────────────────────────────────────────────────────────────
st.subheader("🤖 Asistente")

for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])

pregunta = st.chat_input("Escribe tu pregunta...")
if pregunta:
    st.session_state.chat_history.append({"role": "user", "content": pregunta})
    with st.spinner("Pensando..."):
        try:
            resp = consultar_asistente(pregunta)
        except Exception as e:
            resp = f"Error: {e}"
    st.session_state.chat_history.append(
        {"role": "assistant", "content": resp})
    st.rerun()
