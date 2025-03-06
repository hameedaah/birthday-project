from mailersend import emails
import os
import json
from dotenv import load_dotenv


load_dotenv()


def send_email(to_email, subject, html_content, text_content=""):
    mailer = emails.NewEmail()  

    mail_body = {}
    
    mail_from = {
        "name": "Birthday Reminder System",
        "email": os.getenv("MAILERSEND_SENDER_EMAIL"),  
    }

    recipients = [{"name": "Recipient", "email": to_email}]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html_content, mail_body)
    mailer.set_plaintext_content(text_content, mail_body)

    response = mailer.send(mail_body)
    lines = response.splitlines()

     
    if lines and lines[0].strip() == "422":
        try:
            error_json = json.loads("\n".join(lines[1:]))
            error_detail = error_json.get("errors", {}).get("to", ["Reached trial limit"])[0]
            raise ValueError(error_detail)
        except json.JSONDecodeError:
            raise ValueError("Unable to parse error details.")
        

    if not response.ok:
        raise ValueError("Email sending failed")

    return response