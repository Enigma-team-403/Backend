from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Task
from plyer import notification

def check_alarms():
    now = timezone.now()
    tasks_with_alarms = Task.objects.filter(alarm_time__lte=now, completed=False)
    for task in tasks_with_alarms:
        notification.notify(
            title=f'Alarm for task: {task.title}',
            message=f'This is a reminder for your task: {task.title}. Description: {task.description}.',
            timeout=10
        )
        task.completed = True 
        task.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_alarms, 'interval', minutes=1)
    scheduler.start()
