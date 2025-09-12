# Email Bot 🤖📨

This project is an **AI-powered Gmail assistant** that automatically:
- Fetches new emails from your Gmail inbox
- Keeps track of past email threads
- Uses Hugging Face models (free tier) to generate polite and professional replies
- Sends responses via Gmail
- Labels handled emails with `AI_Replied` to avoid double replies

---

## Features
✅ Gmail API integration  
✅ Hugging Face Inference API (Llama 3.1 8B Instruct by default)  
✅ Conversation history saved locally (`email_history.json`)  
✅ Custom knowledge base (`knowledge_base.txt`)  
✅ Automatic reply formatting with greeting + closing  

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd email_bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Google Cloud Setup
- Create a Google Cloud project
- Enable **Gmail API**
- Download your `credentials.json` and place it inside the project folder
- The first run will open a browser to log in with your Gmail

### 4. Hugging Face Setup
- Get a **READ token** from [Hugging Face Settings](https://huggingface.co/settings/tokens)
- Create an environment variable:
```bash
export HF_API_KEY=hf_xxxxxxxx   # Linux/Mac
setx HF_API_KEY "hf_xxxxxxxx"   # Windows PowerShell
```

---

##Usage

### 1. From another e-mail account, send a test email to your bot’s Gmail address.

### 2. Run the Bot
```bash
python email_bot.py
```

### 3. The bot will:
- Read the latest incoming email.
- Generate a response with AI.
- Send the reply back to the sender.
- Label the message as AI_Replied.

---

## File Structure
```
email_bot/
│── email_bot.py          # Main script
│── credentials.json      # Google API credentials (not committed to Git)
│── token.pickle          # Gmail access/refresh token
│── email_history.json    # Local conversation history
│── knowledge_base.txt    # Optional company knowledge base
│── requirements.txt      # Dependencies
│── README.md             # This file
```

---

## Requirements
- Python 3.10+
- Gmail API access
- Hugging Face API token (read permission)

---

## Example Run
```
🧵 Thread-ID: 1993e75da32c3088

📩 New Email: Interested in gig fuchs_edgar@web.de

🤖 History Text:


🤖 AI Reply:
Hello Dear Matt,

Thank you for your interest in our services. I offer custom solutions in Python automation, web scraping, and AI integrations tailored to meet the specific needs of each project. If you could provide more details about your requirements, I would be happy to assist you further.

Sincerely,
Edgar Fuchs
```

---

## Notes
- Emails are only answered once (using `AI_Replied` label)  
- You can edit `knowledge_base.txt` to add extra context for the AI  
- Conversation history is stored locally per thread  

---
