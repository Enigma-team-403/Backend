from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model to provide standard attributes and functionality
    """
    archived = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        self.archived = True
        self.save()

    class Meta:
        abstract = True



class Message(models.Model):
    room_name = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



