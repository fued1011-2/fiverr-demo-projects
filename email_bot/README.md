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

### 5. Run the Bot
```bash
python email_bot.py
```

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
PS D:\fiverr-demo-projects\email_bot> python email_bot.py
🧵 Thread-ID: 1995318683d23afe


📨 Thread 1995318683d23afe has 3 messages.
   1. John_Doe@gmail.com – Interested in gig
   2. Doe_John@gmail.com – Re: Interested in gig
   3. John_Doe@gmail.com – Re: Interested in gig


🤖 History Text:
 From: John_Doe@gmail.com
Subject: Interested in gig
Message: Hello,

I am interested in a Gig. Where are you located?

Sincerely,
John Doe


From: Doe_John@gmail.com
Subject: Re: Interested in gig
Message: Hello Dear John Doe,

Thank you for your interest in our services. Our main office is located in Berlin, Germany, but we work remotely with clients from all over the world. We can assist you remotely and collaborate via email or video conferencing. Which services from our profile have piqued your interest?

Sincerely,
Doe John


📩 New Email: Re: Interested in gig John_Doe@gmail.com Hello,

Thanks for the reply. What kind of services do you offer?

Sincerely,
John Doe



🤖 AI Reply:
 Hello Dear John Doe,

Our services include Python automation, web scraping, and integrating AI models into existing systems. We also offer custom email automation and bot development, using AI support for Gmail and Outlook. We'd be happy to discuss how we can help you achieve your goals.

Sincerely,
Doe John
```

---

## Notes
- Emails are only answered once (using `AI_Replied` label)  
- You can edit `knowledge_base.txt` to add extra context for the AI  
- Conversation history is stored locally per thread  

---
