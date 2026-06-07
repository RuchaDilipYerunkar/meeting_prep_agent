# MeetMind — AI Meeting Prep Agent 

An AI agent that remembers all your past meetings and generates a smart briefing before your next call. Powered by persistent memory and large language models, MeetMind acts as your expert meeting prep assistant.

## What It Does
* **Persistent Memory:** Stores notes from past conversations into persistent memory, keeping track of facts, promises, and concerns.
* **Smart Recall:** Before any meeting, the agent recalls all semantic and temporal history with that specific contact.
* **Sharp Briefing:** Instantly generates a structured briefing document detailing the contact's background, key topics discussed, unresolved concerns, missed follow-ups, and talking points.

## Tech Stack
* **Backend & Scripting:** Python
* **Web Framework:** Flask
* **Memory Layer:** Hindsight (by Vectorize)
* **LLM Provider:** Groq (LLaMA 3)
* **Frontend UI:** HTML, CSS, and Vanilla JavaScript

## Project Structure
* `mock_data.py`: Feeds fake past meeting transcripts into the memory bank.
* `app.py`: The main command-line interface (CLI) version of the agent.
* `server.py`: The Flask web server that handles API requests and serves the frontend.
* `index.html`: The clean, professional web user interface.
* `.env`: Configuration file for securely storing your API keys.

## Setup & Installation

**1. Set up your environment**
```bash
mkdir meeting-prep-agent
cd meeting-prep-agent
```

**2. Install dependencies**
```bash
pip install groq requests python-dotenv flask hindsight_client
```

**3. Configure API Keys**
Create a new file named exactly `.env` in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_MEMORY_BANK=meeting-prep
```

## How to Run

**Step 1: Ingest Mock Data**
```bash
python mock_data.py
```

**Step 2: Generate Briefings (Web UI)**
```bash
python server.py
```
Open your browser and navigate to `http://localhost:5000`.
