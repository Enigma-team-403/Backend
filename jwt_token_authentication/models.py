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




