# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=30, blank=True, null=True)
#     last_name = models.CharField(max_length=30, blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     birth_date = models.DateField(null=True, blank=True)
#     interesting = models.TextField(blank=True, null=True)
#     job = models.CharField(max_length=50, blank=True, null=True)
#     city = models.CharField(max_length=50, blank=True, null=True)
#     country = models.CharField(max_length=50, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

#     def __str__(self):
        
#         return self.user.username
# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=30, blank=True, null=True)
#     last_name = models.CharField(max_length=30, blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     username = models.CharField(max_length=50, unique=True)
#     birth_date = models.DateField(null=True, blank=True)
#     interesting = models.TextField(blank=True, null=True)
#     job = models.CharField(max_length=50, blank=True, null=True)
#     city = models.CharField(max_length=50, blank=True, null=True)
#     country = models.CharField(max_length=50, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # username = models.CharField(max_length=150, unique=True, null=False, blank=False)

    
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    interesting = models.TextField(blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username  # Use the username from the User model