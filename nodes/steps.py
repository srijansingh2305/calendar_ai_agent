from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from llm_model import llm
from nodes.slots import REQUIRED_SLOTS, all_slots_filled
from nodes.state import AgentState
from calendar_utils import create_event_in_calendar
import json
import re

# ✅ Structured prompt to force JSON
def build_prompt(message: str):
    return [
        HumanMessage(content=(
            f"""You are an assistant that extracts structured meeting information.
Given a user message, extract this as JSON:

- person
- date
- time
- duration
- location
- purpose

Only output valid JSON. No explanation, no prose.
User message: {message}
"""
        ))
    ]

# ✅ LLM step now uses structured prompt and saves result to state
# async def run_llm(state: AgentState) -> AgentState:
#     messages = build_prompt(state.user_input)
#     result = await llm.ainvoke(messages)
#     state.final_answer = result.content
#     return state

async def run_llm(state: AgentState) -> AgentState:
    prompt_messages = build_prompt(state.user_input)
    result = await llm.ainvoke(prompt_messages)
    
    state.chat_history.append(prompt_messages[-1])  # Only add user input
    state.chat_history.append(result)
    
    # Save result for slot extraction
    state.final_answer = result.content
    
    print("🔄 LLM output:", result.content)
    return state


# ✅ Use final_answer instead of re-calling LLM
def extract_slots(state: AgentState) -> AgentState:
    content = state.final_answer
    cleaned = re.sub(r"^```json|```$", "", (content or "").strip(), flags=re.IGNORECASE).strip()

    try:
        parsed = json.loads(cleaned)
        for slot in REQUIRED_SLOTS:
            if slot in parsed:
                state.slots[slot] = parsed[slot]
    except json.JSONDecodeError:
        print("⚠️ Failed to parse cleaned model output as JSON:", cleaned)

    return state

# ✅ Slot validation
def check_completion(state: AgentState) -> AgentState:
    state.all_required_slots_filled = all_slots_filled(state.slots)
    print("🧩 Slot check - all filled?", state.all_required_slots_filled)
    return state

# ✅ Event creation
def create_event(state: AgentState) -> AgentState:
    event_link = create_event_in_calendar(state.slots)
    state.final_answer = f"✅ Event created! [View in Calendar]({event_link})"
    return state





# # nodes/steps.py
# from langchain_core.runnables import RunnableLambda
# from llm_model import llm
# from nodes.slots import REQUIRED_SLOTS, all_slots_filled
# from nodes.state import AgentState
# from calendar_utils import create_event_in_calendar
# from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
# from langchain_core.prompts import ChatPromptTemplate
# import json
# import re


# def build_prompt(message: str):
#     return [
#         HumanMessage(content=(
#             f"""You are an assistant that extracts structured meeting information.
# Given a user message, extract this as JSON:

# - person
# - date
# - time
# - duration
# - location
# - purpose

# Only output valid JSON. No explanation, no prose.
# User message: {message}
# """
#         ))
#     ]

# # --- NEW: Prompt Template for Extraction ---
# llm_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Extract the following fields in JSON: person, date, time, duration, location, purpose."),
#     ("human", "{user_input}")
# ])

# def convert_chat_history(chat_history: list[BaseMessage]) -> list[BaseMessage]:
#     messages = []
#     for msg in chat_history:
#         if isinstance(msg, HumanMessage):
#             messages.append(HumanMessage(content=msg.content))
#         elif isinstance(msg, AIMessage):
#             messages.append(AIMessage(content=msg.content))
#     return messages

# async def run_llm(state: AgentState) -> AgentState:
#     messages = convert_chat_history(state.chat_history) + [HumanMessage(content=state.user_input)]
#     result = await llm.ainvoke(messages)
#     state.chat_history.append(result)
#     print("Messages being sent to LLM:", messages)
#     return state

# # --- FIXED extract_slots ---
# def extract_slots(state: AgentState) -> dict:
#     result = llm.invoke(state.user_input)
#     content = result.content

#     # Strip markdown-style code blocks
#     cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.IGNORECASE).strip()

#     try:
#         parsed = json.loads(cleaned)
#         for slot in REQUIRED_SLOTS:
#             if slot in parsed:
#                 state.slots[slot] = parsed[slot]
#     except json.JSONDecodeError:
#         print("⚠️ Failed to parse cleaned model output as JSON:", cleaned)

#     return {"slots": state.slots}

# def check_completion(state: AgentState) -> AgentState:
#     state.all_required_slots_filled = all_slots_filled(state.slots)
#     print("🧩 Slot check - all filled?", state.all_required_slots_filled)
#     return state



# def create_event(state: AgentState) -> AgentState:
#     event_link = create_event_in_calendar(state.slots)
#     state.final_answer = f"✅ Event created! [View in Calendar]({event_link})"
#     return state
