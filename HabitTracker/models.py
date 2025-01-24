from django.conf import settings
from django.db import models

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')  # استفاده از settings.AUTH_USER_MODEL
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=1)  # تعریف مقدار پیش‌فرض
    goal = models.FloatField()
    progress = models.FloatField(default=0.0)
    topic = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=20, choices=[
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
        ('Others', 'Others'),
    ], default='Others')

    def __str__(self):
        return self.name

    @property
    def daily_target(self):
        if self.duration > 0:
            return self.goal / self.duration
        return 0

class DailyProgress(models.Model):
    habit = models.ForeignKey(Habit, related_name='daily_progress', on_delete=models.CASCADE)
    date = models.DateField()
    completed_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.habit.name} - {self.date}'
