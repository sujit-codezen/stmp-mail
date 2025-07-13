# 📧 Flask SMTP Email API

A secure Flask-based email API using **multiple Gmail SMTP accounts**, with:

- ✅ HTML email support  
- ✅ Multiple recipients  
- ✅ File attachments  
- ✅ Sender account selection (`gmail1`, `gmail2`, etc.)  
- ✅ IP whitelist restriction  
- ✅ Environment variable configuration via `.env`

---

## 🚀 Features

- Send emails using **your Gmail SMTP**
- Choose from multiple accounts dynamically
- Add **attachments**
- Restrict access using IP whitelisting
- Configurable via `.env`

---

## 📁 Project Structure



---

## 🛠️ Setup

### 1. Clone the project

```bash
git clone https://github.com/sujit-codezen/stmp-mail.git
cd flask-smtp-email-api
```


### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure .env
```bash
# Gmail Account 1
GMAIL1_SMTP_SERVER=smtp.gmail.com
GMAIL1_SMTP_PORT=587
GMAIL1_EMAIL=your_account1@gmail.com
GMAIL1_PASSWORD=your_app_password_1

# Gmail Account 2
GMAIL2_SMTP_SERVER=smtp.gmail.com
GMAIL2_SMTP_PORT=587
GMAIL2_EMAIL=your_account2@gmail.com
GMAIL2_PASSWORD=your_app_password_2

# Allowed IPs (comma-separated)
ALLOWED_IPS=127.0.0.1,123.45.67.89
```

## ▶️ Running the Server
```bash
python app.py
```