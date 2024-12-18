from django.db import models
from django.utils import timezone

class List(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # Hex color code

    def __str__(self):  
        return self.name


class Task(models.Model):
    list = models.ForeignKey(List, related_name='tasks', on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    Note= models.CharField(max_length=400)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tasks') 
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)   
    create_time = models.DateField(auto_now_add=True)
    start_task = models.DateField(default=timezone.now)
    end_task = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model): 
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE) 
    text = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self): 
        return f"Comment on {self.task.title} at {self.created_at}"
    

class TaskTag(models.Model):
    task = models.ForeignKey(Task, related_name='task_tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='task_tags', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.title} - {self.tag.name}"
