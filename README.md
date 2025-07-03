# Conversational Calendar Booking Agent

A conversational AI assistant that helps users schedule meetings directly on a connected Google Calendar. The agent understands natural language, extracts meeting details, checks for availability (in future versions), and creates calendar events via API — all through a simple chat interface.

---

## Features

* Natural language understanding using LLM (Gemini, OpenAI, etc.)
* Slot-filling logic for extracting structured data:

  * Person
  * Date
  * Time
  * Duration
  * Location
  * Purpose
* Google Calendar event creation via Service Account
* Multi-turn chat interface (Streamlit)
* Stateless backend with FastAPI
* LangGraph-powered conversational flow control

---

## Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI (Python)
* **Agent Logic:** LangGraph
* **LLM Integration:** Gemini (via LangChain)
* **Calendar Integration:** Google Calendar API (Service Account)
* **Deployment:** Render

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/calendar-ai-agent.git
cd calendar-ai-agent
```

---

### 2. Set up a Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new **Service Account**
3. Generate and download a **JSON key** file
4. Share your target Google Calendar with this service account’s email
5. Note down the **Calendar ID** (e.g. `xyz123@group.calendar.google.com`)

---

### 3. Create `.env` File

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=your-openai-or-gemini-api-key
SERVICE_ACCOUNT_FILE=service_account.json
GOOGLE_CALENDAR_ID=your-calendar-id@group.calendar.google.com
```

---

### 4. Install Dependencies

Make sure you are using Python 3.10 or later.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 5. Run Locally

#### Backend (FastAPI)

```bash
uvicorn app:app --reload
```

Backend runs on `http://localhost:8000`

#### Frontend (Streamlit)

```bash
streamlit run streamlit_app.py
```

Frontend runs on `http://localhost:8501`

---

### 6. API Endpoint

Send a `POST` request to:

```
POST /chat
```

**Payload:**

```json
{
  "message": "Schedule a meeting with Riya tomorrow at 11 AM for 30 minutes in the conference room.",
  "state": {
    "user_input": "...",
    "chat_history": [],
    "slots": {},
    "final_answer": null,
    "tool_calls": []
  }
}
```

---

## Deployment (Render)

### Backend

1. Create a new **Web Service** on [Render](https://render.com/)
2. Connect your repo
3. Use `uvicorn app:app --host 0.0.0.0 --port 8000` as the start command
4. Add your environment variables in the **Render dashboard**

### Frontend

You can deploy Streamlit either:

* On **Streamlit Community Cloud**
* Or create another Render service

Make sure the frontend points to the deployed FastAPI backend like:

```python
API_URL = "https://calendar-ai-agent.onrender.com/chat"
```

---

## To-Do / Future Improvements

* Add slot-filling logic with validation and corrections
* Suggest alternative available time slots
* Allow rescheduling or cancellation
* Store persistent user chat history

---

## License

This project is licensed under the MIT License.

---

## Credits

Built using:

* LangGraph & LangChain
* Google Calendar API
* Gemini / OpenAI LLMs
* FastAPI & Streamlit
