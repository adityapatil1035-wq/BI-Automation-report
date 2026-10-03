import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List
from app.core.config import settings

def send_report_email(
    recipients: List[str],
    subject: str,
    body_html: str,
    attachment_paths: List[str] = None
) -> bool:
    
    if not settings.SMTP_HOST or not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        print(f"[EMAIL SERVICE SIMULATION] SMTP credentials not fully configured. Email queued for recipients: {recipients}")
        print(f"[EMAIL SERVICE SIMULATION] Subject: {subject}")
        print(f"[EMAIL SERVICE SIMULATION] Attachments: {attachment_paths}")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(body_html, 'html'))

        if attachment_paths:
            for path in attachment_paths:
                if os.path.exists(path):
                    filename = os.path.basename(path)
                    with open(path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=filename)
                    part['Content-Disposition'] = f'attachment; filename="{filename}"'
                    msg.attach(part)

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        if settings.SMTP_USE_TLS:
            server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM_EMAIL, recipients, msg.as_string())
        server.quit()
        
        print(f"[EMAIL SERVICE] Successfully sent email to {recipients}")
        return True
    except Exception as e:
        print(f"[EMAIL SERVICE ERROR] Failed to send email: {e}")
        return False
