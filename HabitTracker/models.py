from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class Habit(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(null=True, blank=True, default=7)
    start_date = models.DateField(default=timezone.now)
    goal = models.IntegerField(default=0)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class DailyProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='daily_progress')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.habit.name} - {self.date}'
