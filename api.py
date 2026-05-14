from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from agent.app import build_agent


app = FastAPI(
    title="RPA Agent API",
    version="1.0"
)

agent = build_agent()


class UserRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "RPA Agent API running"
    }


@app.post("/chat")
def chat(req: UserRequest):

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        },
        config=config
    )

    return {
        "response": response["messages"][-1].content
    }