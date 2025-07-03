from fastapi import FastAPI, Request
from graph import calendar_graph
from nodes.state import AgentState

app = FastAPI()

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    user_input = data.get("message")
    state_data = data.get("state", {})

    # Safely override user_input inside state_data
    state_data["user_input"] = user_input
    agent_state = AgentState(**state_data)

    result = await calendar_graph.ainvoke(agent_state, config={"recursion_limit": 50})

    # Ensure result is AgentState
    if isinstance(result, dict):
        result = AgentState(**result)

    return {
        "message": result.final_answer,
        "state": result.dict()
    }


@app.get("/")
def read_root():
    return {"status": "✅ Calendar AI Agent is running."}

