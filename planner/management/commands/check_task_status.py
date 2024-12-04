# myapp/management/commands/check_task_status.py
from django.core.management.base import BaseCommand
from planner.models import Task
from django.utils import timezone

class Command(BaseCommand):
    help = 'Checks and updates the status of tasks'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        tasks = Task.objects.filter(end_time__lte=now, completed=False)
        for task in tasks:
            task.status = 'overdue'
            task.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated task statuses'))
