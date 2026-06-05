import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_MEMORY_BANK")

meetings = [
    """Meeting Date: April 5, 2026
Attendees: Arya, Sarah (Product Manager at TechCorp)
Discussed: Sarah was interested in our analytics dashboard.
She mentioned budget concerns — her team has a cap of $500/month.
She asked about integrations with Slack and Notion.
Promised: Arya to send a Notion integration demo by April 10.
Follow-up missed: Demo was never sent.""",

    """Meeting Date: April 20, 2026
Attendees: Arya, Sarah
Discussed: Sarah followed up asking about the Notion demo.
She also mentioned her team is evaluating 2 competitors: Mixpanel and Amplitude.
She likes our UI but is worried about onboarding time for her 10-person team.
Promised: Arya to share onboarding checklist and case study.
Follow-up missed: Case study was sent but onboarding checklist was not.""",

    """Meeting Date: May 15, 2026
Attendees: Arya, Sarah, Sarah's CTO John
Discussed: John raised concerns about data security and GDPR compliance.
Sarah mentioned they are close to a decision between us and Amplitude.
She asked about pricing for 10 users.
Promised: Arya to send GDPR compliance doc and custom pricing quote.
Follow-up: GDPR doc was sent. Pricing quote was NOT sent."""
]

for i, meeting in enumerate(meetings):
    client.retain(
        bank_id=BANK_ID,
        content=meeting,
        context="sales meeting notes",
        document_id=f"sarah-meeting-{i+1}"
    )
    print(f"Saved memory {i+1} for Sarah ✅")

print("\nAll mock memories saved! Now run app.py")