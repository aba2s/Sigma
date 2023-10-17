from typing import Any
from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule



class Command(BaseCommand):
    help = "Create CRON scheduler tasks "

    def handle(self, *args, **options):
        schedule(
            name='Pulling DSPs and loading data in BDD.',
            func='sigma_app.imports.io_real_spents.upload_io_real_spents',
            # args='request' does not work. To investigate
            # request='request'
            args='request',
            kwargs='',
            schedule_type=Schedule.MINUTES,
            minutes=1,
            repeats=10,
        )
        self.stdout.write(self.style.SUCCESS('CRON task successfully created'))