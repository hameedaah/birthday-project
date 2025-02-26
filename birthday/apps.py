from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit



class BirthdayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'birthday'


    def ready(self):
        import birthday.signals
        # from .tasks import send_birthday_email
        # from pytz import timezone


        # local_tz = timezone("Africa/Lagos")
        # scheduler = BackgroundScheduler()
        # trigger = CronTrigger(hour=9, minute=0, timezone=local_tz)
        # scheduler.add_job(send_birthday_email, trigger)
        # scheduler.start()

        # atexit.register(lambda: scheduler.shutdown())
