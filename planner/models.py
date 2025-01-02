from django.db import models
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default='#FFFFFF')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    alarm_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.completed:
            self.status = 'completed'
        elif self.start_time and self.start_time <= now <= self.end_time:
            self.status = 'in_progress'
        elif self.end_time and now > self.end_time:
            self.status = 'overdue'
        else:
            self.status = 'pending'
        super().save(*args, **kwargs)

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
