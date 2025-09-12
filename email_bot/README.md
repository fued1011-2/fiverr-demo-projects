# Email Bot 🤖📨

This project is an **AI-powered Gmail assistant** that automatically:
- Fetches new emails from your Gmail inbox
- Keeps track of email threads and history
- Uses Hugging Face models (free tier) to generate polite and professional replies
- Sends responses via Gmail
- Labels handled emails with `AI_Replied` to avoid duplicate replies
- Supports a **custom knowledge base** (`knowledge_base.txt`) to enrich replies with company-specific context

---

## ✨ Features
- ✅ Gmail API integration  
- ✅ Hugging Face Inference API (Llama 3.1 8B Instruct by default)  
- ✅ Conversation history stored locally (`email_history.json`)  
- ✅ Extendable **custom knowledge base** (`knowledge_base.txt`)  
- ✅ Automatic reply formatting (greeting + closing)  

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/fued1011-2/fiverr-demo-projects.git
cd email_bot
```

### 2. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 3. Google Cloud Setup
- Create a Google Cloud project  
- Enable **Gmail API**  
- Download your `credentials.json` and place it inside this project folder  
- On first run, a browser will open to log in with your Gmail account  

### 4. Hugging Face Setup
- Generate a **READ token** in your [Hugging Face settings](https://huggingface.co/settings/tokens)  
- Create an environment variable with your token:  
```bash
# Linux/Mac
export HF_API_KEY=hf_xxxxxxxx

# Windows PowerShell
setx HF_API_KEY "hf_xxxxxxxx"
```

---

## ▶️ Usage

1. From **another email account**, send a test email to your bot’s Gmail address.  
   (The bot only replies to emails that actually exist in the inbox.)  

2. Run the bot:
```bash
python email_bot.py
```

3. The bot will:
- Read the latest incoming email  
- Generate a response with AI  
- Send the reply back to the sender  
- Label the email as `AI_Replied`  

---

## 📂 File Structure
```
email_bot/
│── email_bot.py          # Main script
│── credentials.json      # Google API credentials (not committed to Git)
│── token.pickle          # Gmail access/refresh token
│── email_history.json    # Local conversation history
│── knowledge_base.txt    # Optional company knowledge base
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## 📌 Requirements
- Python 3.10+  
- Gmail API access  
- Hugging Face API token (read permission)  

---

## 🖥 Example Run
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

## 📝 Notes
- Emails are only answered **once** (via `AI_Replied` label)  
- You can extend responses by editing `knowledge_base.txt`  
- Conversation history is saved per thread in `email_history.json`  

---
