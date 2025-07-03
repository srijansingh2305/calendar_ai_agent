import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

# ---- Init session state ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "slots" not in st.session_state:
    st.session_state.slots = {}

# ---- Page UI ----
st.set_page_config(page_title="📅 Calendar AI Assistant")
st.title("📅 Conversational Calendar Booking Agent")

chat_container = st.container()
user_input = st.chat_input("What would you like to schedule?")

# ---- When user sends message ----
if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"type": "user", "content": user_input})

    # Build request payload
    payload = {
        "message": user_input,
        "state": {
            "user_input": user_input,
            "chat_history": st.session_state.chat_history,
            "slots": st.session_state.slots,
            "final_answer": None,
            "tool_calls": []
        }
    }

    # ---- Send request to FastAPI backend ----
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            st.error("❌ Backend returned non-JSON response.")
            st.stop()

        # Update slot memory
        st.session_state.slots = data["state"].get("slots", {})

        # Append AI message to history
        if data.get("message"):
            st.session_state.chat_history.append({"type": "ai", "content": data["message"]})

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")
        st.stop()

# ---- Render conversation ----
with chat_container:
    for msg in st.session_state.chat_history:
        role = "assistant" if msg["type"] == "ai" else "user"
        st.chat_message(role).write(msg["content"])
