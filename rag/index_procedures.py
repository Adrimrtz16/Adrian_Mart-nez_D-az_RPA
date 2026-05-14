from pathlib import Path
import json
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# CONFIG

BASE_DIR = Path(__file__).resolve().parent.parent
PROCEDURES_DIR = BASE_DIR / "procedures"
CHROMA_DIR = BASE_DIR / "rag" / "chroma_db"

COLLECTION_NAME = "procedures"

# HELPERS

def workflow_to_document(file_path: Path) -> Document:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    steps_text = " ".join(
        step["type"] for step in data.get("steps", [])
    )

    text = f"""
    id: {data.get("id", "")}

    titulo: {data.get("titulo", "")}

    descripcion: {data.get("descripcion", "")}

    tags:
    {" ".join(data.get("tags", []))}

    parametros:
    {" ".join(data.get("param_schema", {}).keys())}

    acciones:
    {steps_text}

    intencion:
    {data.get("titulo", "").lower()}
    """

    metadata = {
        "id": data["id"],
        "titulo": data["titulo"],
        "file": file_path.name
    }

    return Document(
        page_content=text.strip(),
        metadata=metadata
    )


def load_all_workflows() -> list[Document]:
    """
    Carga todos los workflow.json de procedures/
    """
    docs = []

    files = list(PROCEDURES_DIR.glob("*.workflow.json"))

    if not files:
        raise Exception("No se encontraron workflows en /procedures")

    for file in files:
        print(f"Indexando: {file.name}")
        docs.append(workflow_to_document(file))

    return docs

# MAIN

def main():
    print("\nCargando variables de entorno...")
    load_dotenv()

    print("Cargando workflows...")
    docs = load_all_workflows()

    print("Creando embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Eliminando índice anterior (si existe)...")
    if CHROMA_DIR.exists():
        import shutil
        shutil.rmtree(CHROMA_DIR)

    print("Creando ChromaDB persistente...")
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME
    )

    db.persist()

    print(f"\n✔ {len(docs)} procedimientos indexados correctamente")
    print(f"✔ Base guardada en: {CHROMA_DIR}")


if __name__ == "__main__":
    main()