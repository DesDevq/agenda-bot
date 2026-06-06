import chromadb
from sentence_transformers import SentenceTransformer
import hashlib

modelo = SentenceTransformer("all-MiniLM-L6-v2")
cliente = chromadb.PersistentClient(path="./chroma_db")
coleccion = cliente.get_or_create_collection(
    name="tareas_usuario",
    metadata={"hnsw:space": "cosine"}
)


def guardar_tarea(mensaje_original: str, tarea: str):
    embedding = modelo.encode(mensaje_original).tolist()
    id_unico = hashlib.md5(mensaje_original.encode()).hexdigest()

    coleccion.upsert(
        embeddings=[embedding],
        documents=[tarea],
        metadatas=[{"mensaje": mensaje_original}],
        ids=[id_unico]
    )
    print(f"💾 Tarea guardada en ChromaDB")


def buscar_tareas_similares(mensaje: str, n: int = 3) -> str:
    embedding = modelo.encode(mensaje).tolist()

    try:
        results = coleccion.query(
            query_embeddings=[embedding],
            n_results=n
        )
        tareas = results["documents"][0] if results["documents"] else []
        if not tareas:
            return "Sin tareas previas."
        return "\n".join([f"- {t}" for t in tareas])
    except Exception:
        return "Sin tareas previas."


def guardar_documento(nombre: str, contenido: str):
    coleccion_docs = cliente.get_or_create_collection(
        name="documentos_usuario",
        metadata={"hnsw:space": "cosine"}
    )

    # mejora del RAG
    # Mejora: chunking por párrafos en vez de caracteres fijos
    parrafos = [p.strip() for p in contenido.split("\n\n") if p.strip()]

    # Si algún párrafo es muy largo, lo subdivide
    chunks = []
    for parrafo in parrafos:
        if len(parrafo) <= 600:
            chunks.append(parrafo)
        else:
            # Subdivide párrafos largos en oraciones
            oraciones = parrafo.split(". ")
            chunk_actual = ""
            for oracion in oraciones:
                if len(chunk_actual) + len(oracion) <= 600:
                    chunk_actual += oracion + ". "
                else:
                    if chunk_actual:
                        chunks.append(chunk_actual.strip())
                    chunk_actual = oracion + ". "
            if chunk_actual:
                chunks.append(chunk_actual.strip())

    for i, chunk in enumerate(chunks):
        embedding = modelo.encode(chunk).tolist()
        id_unico = hashlib.md5(f"{nombre}-{i}".encode()).hexdigest()
        coleccion_docs.upsert(
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"nombre": nombre, "chunk": i}],
            ids=[id_unico]
        )
    print(
        f"💾 Documento '{nombre}' guardado ({len(chunks)} chunks por párrafos)")


def buscar_en_documentos(pregunta: str, n: int = 3) -> str:
    coleccion_docs = cliente.get_or_create_collection(
        name="documentos_usuario",
        metadata={"hnsw:space": "cosine"}
    )
    embedding = modelo.encode(pregunta).tolist()
    try:
        results = coleccion_docs.query(
            query_embeddings=[embedding],
            n_results=n
        )
        docs = results["documents"][0] if results["documents"] else []
        if not docs:
            return "Sin documentos relevantes."
        return "\n".join([f"- {d}" for d in docs])
    except Exception:
        return "Sin documentos relevantes."
