from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from .tasks import send_birthday_emails


class BirthdayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'birthday'

    # def ready(self):
    #         scheduler = BackgroundScheduler(timezone="UTC")
    #         scheduler.add_job(
    #             send_birthday_emails,
    #             # trigger=CronTrigger(hour="0", minute="5"),
    #             trigger=IntervalTrigger(minutes=1),
    #             id="send_birthday_emails",
    #             replace_existing=True
    #         )
    #         scheduler.start()
