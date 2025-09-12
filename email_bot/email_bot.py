import base64
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests


# -------------------------------
# SETUP
# -------------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_API_KEY_HERE")
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

HISTORY_FILE = Path("email_history.json")
KNOWLEDGE_BASE = Path("knowledge_base.txt")


# -------------------------------
# HUGGING FACE GENERATION
# -------------------------------
def hf_generate(history_text: str, subject: str, body: str, knowledge: str = KNOWLEDGE_BASE):
    """Generate an AI response using Hugging Face chat completions API."""
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    # Build chat messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI email assistant for the freelancer Edgar Fuchs. "
                "Always write short, polite and professional replies. "
                "Start with 'Hello Dear (Name of the Client),' and end with 'Sincerely, Edgar Fuchs'. "
                "Do not include the subject line in your response."
            )
        }
    ]

    if history_text:
        messages.append({"role": "system", "content": f"Conversation so far:\n{history_text}"})

    if knowledge:
        messages.append({"role": "system", "content": f"Company knowledge base:\n{knowledge}"})

    # Add the latest email
    messages.append({
        "role": "user",
        "content": f"Subject: {subject}\nMessage: {body}"
    })

    data = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",  # Free and powerful LLM
        "messages": messages,
        "max_tokens": 400
    }

    response = requests.post(HF_API_URL, headers=headers, json=data, timeout=90)

    if response.status_code == 200:
        try:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"⚠️ Error parsing HF response: {e}\nRaw: {response.text}"
    else:
        return f"⚠️ HF API Error {response.status_code}: {response.text}"


# -------------------------------
# HISTORY MANAGEMENT
# -------------------------------
def load_knowledge_base():
    """Load optional company knowledge base from file."""
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _load_history():
    """Load conversation history from JSON file."""
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def _save_history(history: dict):
    """Save conversation history to JSON file."""
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def append_history(thread_id: str, role: str, text: str):
    """Append a new message to the history for a given thread."""
    h = _load_history()
    h.setdefault(thread_id, []).append({"role": role, "text": text})
    _save_history(h)


def get_history_text(thread_id: str, max_turns: int = 6) -> str:
    """Return the last N turns of the conversation as plain text."""
    h = _load_history()
    turns = h.get(thread_id, [])[-max_turns:]
    return "\n".join(f"{m['role'].upper()}: {m['text']}" for m in turns)


# -------------------------------
# GMAIL HELPERS
# -------------------------------
def get_gmail_service():
    """Authenticate and return the Gmail API service client."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def get_latest_email(service):
    """Fetch the latest unread email that has not been AI-replied yet."""
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q="-label:AI_Replied",
        maxResults=1
    ).execute()

    if "messages" not in results:
        return None

    msg_id = results['messages'][0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id).execute()

    thread_id = str(msg['threadId'])
    payload = msg['payload']
    headers = payload['headers']

    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "(no subject)")
    sender = next((h['value'] for h in headers if h['name'] == 'From'), "(unknown sender)")

    if "parts" in payload:
        body_data = payload['parts'][0]['body'].get("data")
    else:
        body_data = payload['body'].get("data")

    if body_data:
        body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
    else:
        body = "(no text content found)"

    return subject, sender, body, thread_id, msg_id


def extract_body(payload):
    """Extract plain text or HTML content from a Gmail message payload."""
    body = "(no content)"

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            data = part["body"].get("data")
            if not data:
                continue

            decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

            if mime_type == "text/plain":
                return decoded.strip()
            elif mime_type == "text/html":
                soup = BeautifulSoup(decoded, "html.parser")
                body = soup.get_text().strip()
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return body


def get_thread_conversation(service, thread_id, max_msgs=3):
    """Fetch the last N messages of a thread (excluding the newest one)."""
    thread = service.users().threads().get(userId="me", id=thread_id).execute()
    messages = thread.get("messages", [])

    print(f"📨 Thread {thread_id} has {len(messages)} messages.")

    # Use the subject of the first message as fallback
    first_hdrs = messages[0]["payload"]["headers"]
    thread_subject = next((h['value'] for h in first_hdrs if h['name'] == 'Subject'), "Re: (no subject)")

    for i, m in enumerate(messages, 1):
        hdrs = m["payload"]["headers"]
        sender = next((h["value"] for h in hdrs if h["name"] == "From"), "(unknown sender)")
        subject = next((h['value'] for h in hdrs if h['name'] == 'Subject'), None)

        if not subject:
            subject = "Re: " + thread_subject

        print(f"   {i}. {sender} – {subject}")

    print("\n")

    if len(messages) <= 1:
        return ""

    previous_msgs = messages[:-1]
    selected = previous_msgs[-max_msgs:]

    conversation = []
    for m in selected:
        payload = m.get("payload", {})
        headers = payload.get("headers", [])
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)

        if not subject:
            subject = "Re: " + thread_subject

        body = extract_body(payload)
        conversation.append(f"From: {sender}\nSubject: {subject}\nMessage: {body}\n")

    return "\n".join(conversation)


# -------------------------------
# EMAIL ACTIONS
# -------------------------------
def create_ai_response(subject, body, history_text="", knowledge=""):
    """Wrapper to call Hugging Face for AI reply generation."""
    return hf_generate(history_text, subject, body, knowledge)


def send_email(service, to, subject, body_text, thread_id=None):
    """Send an email reply through Gmail API."""
    message = MIMEText(body_text)
    message['to'] = to
    message['from'] = "me"
    if subject.lower().startswith(("re:", "fwd:")):
        message['subject'] = subject
    else:
        message['subject'] = "Re: " + subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    if thread_id:
        body['threadId'] = thread_id

    service.users().messages().send(userId="me", body=body).execute()


def add_label(service, msg_id, label_name="AI_Replied"):
    """Add a custom label to mark that this email has been handled by AI."""
    labels = service.users().labels().list(userId='me').execute()
    label_id = None
    for lbl in labels['labels']:
        if lbl['name'] == label_name:
            label_id = lbl['id']
            break

    if not label_id:
        label = {'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
        new_label = service.users().labels().create(userId='me', body=label).execute()
        label_id = new_label['id']

    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': [label_id]}
    ).execute()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == '__main__':
    service = get_gmail_service()
    latest = get_latest_email(service)
    if latest:
        subject, sender, body, thread_id, msg_id = latest
        print("🧵 Thread-ID:", thread_id)
        print("\n")

        history_text = get_thread_conversation(service, thread_id, max_msgs=3)

        print("🤖 History Text:\n", history_text)
        print("\n")

        print("📩 New Email:", subject, sender, body)
        print("\n")

        knowledge = load_knowledge_base()
        ai_reply = create_ai_response(subject, body, history_text, knowledge)
        print("🤖 AI Reply:\n", ai_reply)

        append_history(thread_id, "user", f"From {sender}: {body}")
        append_history(thread_id, "assistant", ai_reply)

        send_email(service, sender, subject, ai_reply, thread_id)
        add_label(service, msg_id, "AI_Replied")
    else:
        print("No new emails found.")
