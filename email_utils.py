import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

def send_email(to_emails, subject, html_content, sender_account="gmail1", attachment_paths=None):
    accounts = {
        "gmail1": {
            "smtp_server": os.getenv("GMAIL1_SMTP_SERVER"),
            "smtp_port": int(os.getenv("GMAIL1_SMTP_PORT")),
            "email": os.getenv("GMAIL1_EMAIL"),
            "password": os.getenv("GMAIL1_PASSWORD"),
        }
    }

    if sender_account not in accounts:
        return {"error": f"Unknown sender account '{sender_account}'"}

    account = accounts[sender_account]

    if isinstance(to_emails, str):
        to_emails = [to_emails]

    message = MIMEMultipart()
    message["From"] = account["email"]
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    if attachment_paths:
        for path in attachment_paths:
            try:
                with open(path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(path))
                    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
                    message.attach(part)
            except Exception as e:
                return {"error": f"Failed to attach {path}: {e}"}

    try:
        with smtplib.SMTP(account["smtp_server"], account["smtp_port"]) as server:
            server.starttls()
            server.login(account["email"], account["password"])
            server.sendmail(account["email"], to_emails, message.as_string())
        return {"message": f"Email sent successfully from {account['email']}"}
    except Exception as e:
        return {"error": str(e)}
