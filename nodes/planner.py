# nodes/planner.py
from llm_model import llm

def extract_slots(user_input: str) -> dict:
    prompt = f"""Extract calendar booking info from the message below:
Message: "{user_input}"

Return JSON with fields:
- title
- date (YYYY-MM-DD)
- time (HH:MM)
- duration (minutes)
- attendees (comma-separated emails or names)
- location

If not found, leave fields empty.
"""
    response = llm._call(prompt)
    try:
        return eval(response)  # Replace with `json.loads()` in prod if response is valid JSON
    except:
        return {}
