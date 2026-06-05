import os
import uuid
import asyncio
import nest_asyncio
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from dotenv import load_dotenv
from hindsight_client import Hindsight

nest_asyncio.apply()
load_dotenv()

app = Flask(__name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)
BANK_ID = os.getenv("HINDSIGHT_MEMORY_BANK")

def get_memory(contact_name):
    response = hindsight.recall(
        bank_id=BANK_ID,
        query=f"past meetings with {contact_name}"
    )
    if not response.results:
        return "", 0
    memories = "\n\n".join([r.text for r in response.results])
    return memories, len(response.results)

def generate_briefing_text(contact_name):
    past, count = get_memory(contact_name)
    if not past:
        return None, 0

    prompt = f"""You are an expert meeting prep assistant.

Below are notes from all past meetings with {contact_name}.
Generate a clean, professional briefing document for today's call.

Structure it with these exact sections:
1. Background
   Quick summary of who {contact_name} is and their company.

2. Key Topics Discussed
   What has been covered in past meetings.

3. Unresolved Concerns
   Any objections, worries, or open questions they raised.

4. Missed Follow-Ups
   Promises that were made but NOT fulfilled yet.

5. Talking Points for Today
   What to lead with in today's call.

6. Questions to Ask
   3-4 smart questions to ask {contact_name} today.

PAST MEETING NOTES:
{past}

Generate the briefing now:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, count

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/briefing")
def briefing():
    contact = request.args.get("contact", "").strip()
    if not contact:
        return jsonify({"error": "Please enter a contact name."}), 400
    try:
        text, count = generate_briefing_text(contact)
        if not text:
            return jsonify({"error": f"No past meetings found for '{contact}'. Add a meeting first!"}), 404
        return jsonify({"briefing": text, "memory_count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/save-meeting", methods=["POST"])
def save_meeting():
    data = request.get_json()
    contact = (data.get("contact") or "").strip()
    notes = (data.get("notes") or "").strip()
    date = (data.get("date") or "").strip()

    if not contact or not notes:
        return jsonify({"error": "Contact name and meeting notes are required."}), 400

    try:
        doc_id = f"{contact.lower().replace(' ','-')}-{str(uuid.uuid4())[:8]}"
        content = f"Meeting Date: {date}\nContact: {contact}\n\n{notes}"

        hindsight.retain(
            bank_id=BANK_ID,
            content=content,
            context="meeting notes",
            document_id=doc_id
        )
        return jsonify({"success": True, "message": f"Meeting with {contact} saved to memory!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n========================================")
    print("  MeetMind — Meeting Prep Agent UI")
    print("========================================")
    print("  Open this in your browser:")
    print("  http://localhost:5000")
    print("========================================\n")
    app.run(debug=False, port=5000)