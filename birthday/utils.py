from mailersend import emails
import os
from dotenv import load_dotenv


load_dotenv()


def send_email(to_email, template_id, personalization_data, subject=None):
    mailer = emails.NewEmail()
    mail_body = {}

    mail_from = {
        "name": "Birthday Reminder System",
        "email": os.getenv("MAILERSEND_SENDER_EMAIL"),
    }

    recipients = [
        {
            "name": "Recipient",
            "email": to_email,
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_template(template_id, mail_body)
    if subject:
        mailer.set_subject(subject, mail_body)
    personalization = [
        {
            "email": to_email,
            "data": personalization_data
        }
    ]
    mailer.set_personalization(personalization, mail_body)

    response = mailer.send(mail_body)
    return response