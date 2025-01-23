from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DailyProgress, Habit
from django.core.cache import cache

@receiver(post_save, sender=DailyProgress)
def update_community_progress(sender, instance, **kwargs):
    habit = instance.habit
    completed_days = habit.daily_progress.filter(completed=True).count()
    progress_percentage = (completed_days / habit.duration) * 100 if habit.duration > 0 else 0

    habit.progress = progress_percentage
    habit.save()

    # به‌روزرسانی در کش
    cache.set(f'habit_{habit.id}_progress', progress_percentage)
