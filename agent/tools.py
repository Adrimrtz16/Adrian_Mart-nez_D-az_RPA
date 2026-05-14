from pathlib import Path
import json
import os

from dotenv import load_dotenv

from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI


# CONFIG

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROCEDURES_DIR = BASE_DIR / "procedures"
CHROMA_DIR = BASE_DIR / "rag" / "chroma_db"


# CARGA RAG

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings,
    collection_name="procedures"
)

# LLM

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

# TOOL 1: SEARCH PROCEDURES

@tool
def search_procedures(query: str) -> list:
    """
    Busca en la base RAG el procedimiento más adecuado para una petición
    del usuario escrita en lenguaje natural.

    Usar esta tool siempre que haya que decidir qué workflow ejecutar.
    """
    results = vector_db.similarity_search_with_score(query, k=3)

    output = []

    for doc, score in results:
        workflow_path = PROCEDURES_DIR / doc.metadata["file"]

        with open(workflow_path, encoding="utf-8") as f:
            wf = json.load(f)

        output.append({
            "id": doc.metadata["id"],
            "titulo": doc.metadata["titulo"],
            "score": float(score),
            "param_schema": wf["param_schema"]
        })

    return output

# TOOL 2: LIST PROCEDURES

@tool
def list_procedures() -> list:
    """
    Devuelve todos los procedimientos disponibles.

    Útil cuando la petición del usuario es ambigua y el agente
    necesita orientarse antes de elegir uno.
    """
    workflows = []

    for file in PROCEDURES_DIR.glob("*.workflow.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        workflows.append({
            "id": data["id"],
            "titulo": data["titulo"],
            "descripcion": data["descripcion"]
        })

    return workflows

# TOOL 3: EXTRACT PARAMETERS

@tool
def extract_parameters(user_request: str, param_schema: dict) -> dict:
    """
    Extrae los parámetros necesarios para ejecutar un workflow
    a partir de una petición en lenguaje natural.
    """

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    prompt = f"""
Extrae estos parámetros desde la petición del usuario.

Schema:
{json.dumps(param_schema, indent=2)}

Petición:
{user_request}

Devuelve SOLO JSON válido.
No añadas texto.
"""

    response = llm.invoke(prompt).content.strip()

    # quitar fences markdown
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # localizar primer y último {}
    start = response.find("{")
    end = response.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError(
            f"No se pudo parsear JSON: {response}"
        )

    clean_json = response[start:end]

    return json.loads(clean_json)

# TOOL 4: RUN WORKFLOW

@tool
def run_workflow(workflow_id: str, parameters: dict) -> dict:
    """
    Ejecuta un workflow RPA usando su id y los parámetros extraídos.

    Rellena placeholders y lanza el navegador para automatizar
    el formulario web.
    """
    from agent.runner import run_workflow_file

    result = run_workflow_file(
        workflow_id=workflow_id,
        parameters=parameters
    )

    return result