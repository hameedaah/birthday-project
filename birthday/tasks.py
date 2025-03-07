from .utils import send_email
from datetime import date
from .models import Staff, NotificationLog  
from django.template.loader import render_to_string

def compute_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def send_birthday_email():
    today = date.today()

    staff_with_birthday = Staff.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        is_enabled=True
    ).select_related('notification_template')

    
    for staff in staff_with_birthday:
        message = staff.notification_template.message.strip()
        if not message.strip():
            message = "Happyy Birthday! Wishing you a fantastic day full of joy and success."

        personalization_data = {
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "age": str(compute_age(staff.date_of_birth)),
            "month": staff.date_of_birth.strftime("%B"),  
            "day": str(staff.date_of_birth.day),
            "message": message
        }

        template_id = "pq3enl6q10842vwr"  

        try:
            response = send_email(
                to_email=staff.email,
                template_id=template_id,
                personalization_data=personalization_data,
                subject="Happy Birthday!"
            )
            NotificationLog.objects.create(staff=staff, status='sent', error_message='')
        except Exception as e:
            NotificationLog.objects.create(staff=staff, status='failed', error_message=str(e))