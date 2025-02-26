# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Staff, NotificationTemplate

@receiver(post_save, sender=Staff)
def create_notification_template(sender, instance, created, **kwargs):
    if created:
        NotificationTemplate.objects.create(staff=instance)
