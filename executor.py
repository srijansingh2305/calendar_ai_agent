# executor.py

from fastapi import FastAPI, Request
from graph import calendar_graph
from nodes.state import AgentState

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(req: Request):
    data = await req.json()
    user_input = data.get("input", "")

    state = AgentState(
        user_input=user_input,
        chat_history=[],
        slots={},
        final_answer=None,
        tool_calls=[]
    )
    result = calendar_graph.invoke(state)
    return {"response": result.final_answer}
