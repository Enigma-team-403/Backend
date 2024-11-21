from django.db import models
from django.utils import timezone
    
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default='#FFFFFF')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    alarm_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        
        return self.title
    
    

class ChecklistItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]
