# tasks.py
from .utils import send_email
from datetime import date
from .models import Staff, NotificationLog  


def send_birthday_email():
    today = date.today()

    staff_with_birthday = Staff.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        is_enabled=True
    ).select_related('notification_template')

    
    for staff in staff_with_birthday:
        message = staff.notification_template.message
        # Fallback to default message if message is empty
        if not message.strip():
            message = "Happy Birthday! Wishing you a fantastic day full of joy and success."
        subject = "Happy Birthday!"
        html_content = f"<h1>Happy Birthday, {staff.first_name}!</h1><p>{message}</p>"
        text_content = f"Happy Birthday, {staff.first_name}! {message}"
        
        try:
            # Send the email
            response = send_email(
                to_email=staff.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
 
            # Log success
            NotificationLog.objects.create(staff=staff, status='sent', error_message='')
        except Exception as e:
            # Log failure with error message
            NotificationLog.objects.create(staff=staff, status='failed', error_message=str(e))

