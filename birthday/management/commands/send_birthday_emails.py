from django.core.management.base import BaseCommand
from birthday.tasks import send_birthday_email

class Command(BaseCommand):
    help = "Send birthday emails to staff"

    def handle(self, *args, **kwargs):
        send_birthday_email()