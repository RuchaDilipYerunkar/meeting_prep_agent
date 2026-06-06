# Contributed by Anushree Bonde
import os
from groq import Groq
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

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
        return ""
    return "\n\n".join([r.text for r in response.results])

def generate_briefing(contact_name):
    print(f"\nFetching memory for {contact_name}...")
    past = get_memory(contact_name)

    if not past:
        print("No past meetings found for this contact.")
        return

    prompt = f"""You are an expert meeting prep assistant.

Below are notes from all past meetings with {contact_name}.
Generate a clean, professional briefing document for today's call.

Include:
1. Quick background on {contact_name}
2. Key topics discussed in past meetings
3. Unresolved concerns or objections
4. Missed follow-ups (promises not kept)
5. Recommended talking points for today
6. Suggested questions to ask

PAST MEETING NOTES:
{past}

Generate the briefing now:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    briefing = response.choices[0].message.content

    filename = f"briefing_{contact_name.lower()}.txt"
    with open(filename, "w") as f:
        f.write(f"MEETING BRIEFING: {contact_name}\n")
        f.write("="*50 + "\n\n")
        f.write(briefing)

    print(f"\n{'='*50}")
    print(f"MEETING BRIEFING FOR: {contact_name.upper()}")
    print('='*50)
    print(briefing)
    print(f"\n✅ Briefing saved to: briefing_{contact_name.lower()}.txt")

print("=== Meeting Prep Agent ===")
contact = input("Who is your meeting with today? ").strip()
generate_briefing(contact)
