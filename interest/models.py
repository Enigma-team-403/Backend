from django.db import models
from django.conf import settings

class Interest(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class UserInterest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.interest.name}'


from .models import Interest

def create_interests():
    interests_data = [
        {"name": "Music", "category": "Entertainment"},
        {"name": "Sports", "category": "Health"},
        {"name": "Technology", "category": "Science"},
        {"name": "Books", "category": "Education"},
        {"name": "Travel", "category": "Lifestyle"}
    ]

    for data in interests_data:
        interest, created = Interest.objects.get_or_create(name=data["name"], category=data["category"])
        if created:
            print(f'Interest "{interest.name}" created successfully.')
        else:
            print(f'Interest "{interest.name}" already exists.')

# اجرای تابع برای ایجاد علاقه‌مندی‌ها
# create_interests()
