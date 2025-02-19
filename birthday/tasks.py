# tasks.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def send_birthday_emails():
    """
    Query for birthdays that match today's date and send out an email
    to each recipient.
    """
    from .models import Birthday
    today = timezone.now().date()
    birthdays_today = Birthday.objects.filter(birth_date=today)

    for birthday in birthdays_today:
        # If Birthday model has a ForeignKey to User with an email field.
        if birthday.user and birthday.user.email:
            recipient_email = birthday.user.email
        else:
            # Alternatively, if your Birthday model stores email directly,
            # recipient_email = birthday.email
            continue  # Skip if no email found

        subject = "Happy Birthday!"
        message = (
            'happy birthday.'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [recipient_email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent birthday email to {recipient_email}")
