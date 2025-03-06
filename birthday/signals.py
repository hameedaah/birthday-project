# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Staff, NotificationTemplate
from django.conf import settings

@receiver(post_save, sender=Staff)
def create_notification_template(sender, instance, created, **kwargs):
    if created:
        NotificationTemplate.objects.create(staff=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def link_staff_record(sender, instance, created, **kwargs):
    if created and instance.is_staff and not instance.is_superuser:
        staff = Staff.objects.filter(email=instance.email, user__isnull=True).first()
        if staff:
            staff.user = instance  # Link the staff record to the user
            staff.save(update_fields=["user"])
