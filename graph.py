# graph.py
from langgraph.graph import StateGraph, END
from nodes.state import AgentState
from nodes.steps import (
    run_llm,
    extract_slots,
    check_completion,
    create_event,
)

builder = StateGraph(AgentState)

builder.add_node("llm", run_llm)
builder.add_node("extract", extract_slots)
builder.add_node("check", check_completion)
builder.add_node("create", create_event)

builder.set_entry_point("llm")

builder.add_edge("llm", "extract")
builder.add_edge("extract", "check")
builder.add_conditional_edges(
    "check",
    lambda s: "create" if s.all_required_slots_filled else "llm",
)




builder.add_edge("create", END)

calendar_graph = builder.compile()

