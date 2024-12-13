from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')

    def __str__(self):
        return self.name


class Community(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='communities')
    profile_picture = models.ImageField(upload_to='profile_community/', null=True, blank=True)
    external_habits = models.ManyToManyField('HabitTracker.Habit', related_name='linked_communities', blank=True)

    def __str__(self):
        return self.title