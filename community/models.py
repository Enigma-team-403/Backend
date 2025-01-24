from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from HabitTracker.models import Habit


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Community(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    habits = models.ManyToManyField(Habit, related_name='communities')
    categories = models.ManyToManyField(Category, related_name='communities')
    profile_picture = models.ImageField(upload_to='profile_community/', null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communities', blank=True)
    profile_picture = models.ImageField(upload_to='community_profiles/', null=True, blank=True)
    def __str__(self):
        return self.title
    


class MembershipRequest(models.Model): 
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='membership_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    selected_habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Request from {self.requester} to {self.community.name} ({self.status})"


