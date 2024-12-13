from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import User

@receiver(user_logged_in)
def update_last_active(sender, request, user, **kwargs):
    user.last_active = timezone.now()
    user.save()
