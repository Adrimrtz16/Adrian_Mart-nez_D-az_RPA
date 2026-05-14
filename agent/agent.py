import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from agent.tools import (
    search_procedures,
    extract_parameters,
    run_workflow,
    list_procedures
)


load_dotenv()


SYSTEM_PROMPT = """
Eres un agente RPA especializado en automatizar formularios web.

Siempre debes trabajar usando tools.

Proceso obligatorio:

1. Llama SIEMPRE primero a search_procedures con la petición del usuario.
2. Elige el procedimiento con mejor score.
3. Después llama SIEMPRE a extract_parameters usando:
   - la petición original del usuario
   - el param_schema del procedimiento elegido
4. Si extract_parameters devuelve todos los parámetros requeridos,
   llama inmediatamente a run_workflow.
5. Si falta alguno, pregunta exactamente cuál falta.
6. No inventes parámetros.
7. No respondas directamente sin usar tools.

Si search_procedures devuelve varios resultados,
debes elegir SIEMPRE el primero (mejor score).
"""


def build_agent():

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    memory = MemorySaver()

    agent = create_react_agent(
        llm,
        tools=[
            search_procedures,
            extract_parameters,
            run_workflow,
            list_procedures
        ],
        checkpointer=memory,
        prompt=SYSTEM_PROMPT
    )

    return agent