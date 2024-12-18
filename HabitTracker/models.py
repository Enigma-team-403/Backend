from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,related_name='tracker_habits', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
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
