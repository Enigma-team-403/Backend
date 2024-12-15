# community/models.py

from django.db import models
from django.conf import settings  # Import settings to reference the custom user model

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    duration_days = models.IntegerField()  # Duration of the habit in days

    def __str__(self):
        return self.name


class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use the custom user model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True, blank=True)  # Linking the Habit model to the Community model

    def __str__(self):
        return self.name
