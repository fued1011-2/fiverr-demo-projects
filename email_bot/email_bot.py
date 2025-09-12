import base64
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import google.generativeai as genai
import json
from pathlib import Path


# -------------------------------
# SETUP
# -------------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# -load Gemini API-Key (either as environment variable or as plain text here)
API_KEY = os.getenv("GEMINI_API_KEY", "DEIN_API_KEY_HIER")  
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

HISTORY_FILE = Path("email_history.json")

def _load_history():
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def _save_history(history: dict):
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8"
    )

def append_history(thread_id: str, role: str, text: str):
    """role: 'user' oder 'assistant'"""
    h = _load_history()
    h.setdefault(thread_id, []).append({"role": role, "text": text})
    _save_history(h)

def get_history_text(thread_id: str, max_turns: int = 6) -> str:
    """Gibt die letzten N Turns formatiert zurück."""
    h = _load_history()
    turns = h.get(thread_id, [])[-max_turns:]
    return "\n".join(f"{m['role'].upper()}: {m['text']}" for m in turns)


def get_gmail_service():
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
    results = service.users().messages().list(
        userId='me', maxResults=1, labelIds=['INBOX']
    ).execute()
    messages = results.get('messages', [])
    if not messages:
        return None
    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    thread_id = msg.get('threadId')
    payload = msg['payload']
    headers = payload['headers']
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')
    sender = next(h['value'] for h in headers if h['name'] == 'From')

    if 'parts' in payload:
        body_data = payload['parts'][0]['body'].get('data')
    else:
        body_data = payload['body'].get('data')

    if body_data:
        body = base64.urlsafe_b64decode(body_data).decode('utf-8')
    else:
        body = "(Kein Textinhalt gefunden)"

    return subject, sender, body, thread_id



def create_ai_response(subject, body, history_text=""):
    prompt = f"""
        You are an AI email assistant. Write a short, polite and professional reply.

        Conversation so far (most recent first):
        {history_text or "(no prior messages)"}

        New email:
        Subject: {subject}
        Message: {body}
    """
    response = model.generate_content(prompt)
    return response.text


def send_email(service, to, subject, body_text):
    message = MIMEText(body_text)
    message['to'] = to
    message['from'] = "me"
    message['subject'] = "Re: " + subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw}).execute()


# -------------------------------
# MAIN
# -------------------------------
if __name__ == '__main__':
    service = get_gmail_service()
    latest = get_latest_email(service)
    if latest:
        subject, sender, body, thread_id = latest
        print("📩 Neue Mail:", subject, sender)

        # 1) Bisherige History für diesen Thread holen
        history_text = get_history_text(thread_id)

        # 2) Antwort generieren (mit History)
        ai_reply = create_ai_response(subject, body, history_text)
        print("🤖 KI Antwort:\n", ai_reply)

        # 3) Verlauf aktualisieren
        append_history(thread_id, "user", f"From {sender}: {body}")
        append_history(thread_id, "assistant", ai_reply)

        # 4) Senden (optional – zum Testen lieber erstmal auslassen)
        # send_email(service, sender, subject, ai_reply)
        print("⚠️ Demo-Modus: E-Mail NICHT gesendet. (send_email() auskommentiert)")
    else:
        print("Keine neuen Mails gefunden.")
