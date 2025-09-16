# Fiverr Demo Projects (Python)

This repository contains small Python demo projects that showcase my skills
in automation, web scraping, API integration, and AI-powered assistants —  
the same services I offer on Fiverr.

---

## 📂 Projects

### 1. CSV/Excel Cleaner
- Removes duplicate rows  
- Drops empty columns  
- Saves cleaned data to CSV/Excel  

### 2. Web Scraper Demo
- Scrapes quotes and authors from a sample website  
- Exports results to CSV  

### 3. API Integration Demo
- Fetches weather data from the free Open-Meteo API  
- Saves results to CSV  

### 4. Email Bot (NEW 🚀)
- Connects to your Gmail inbox via the Gmail API  
- Uses Hugging Face LLMs (Llama-3.1-8B-Instruct) to automatically generate replies  
- Keeps track of past messages in a thread (conversation history)  
- Adds a Gmail label (`AI_Replied`) to avoid duplicate responses  
- Supports a **custom knowledge base** (`knowledge_base.txt`) that is included in replies  

👉 Full setup instructions are in [`email_bot/README.md`](./email_bot/README.md)

---

## ⚙️ Installation

Clone the repository and install the requirements:

```bash
git clone https://github.com/DEINUSER/fiverr-demo-projects.git
cd fiverr-demo-projects
pip install -r requirements.txt
```

---

## ▶️ Usage

Each project has its own folder with a script and README.  
Example (CSV Cleaner):

```bash
cd csv_cleaner
python csv_cleaner.py
```

Example (Email Bot):  
👉 First, send a test email to your Gmail account from another address, then run:

```bash
cd email_bot
python email_bot.py
```

---

## 💼 Fiverr

Need a custom solution in Python automation, scraping, API integration, or AI bots?  
👉 **My Fiverr profile:** [https://www.fiverr.com/xdisslike](https://www.fiverr.com/xdisslike)