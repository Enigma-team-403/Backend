# from django.apps import AppConfig


# class ProfilesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'profiles'

# planner/profiles/apps.py
from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'planner.profiles'  # This should be the full Python path to the app
