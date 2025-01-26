from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DailyProgress, Habit
from community.models import MembershipRequest
from django.core.cache import cache
import requests

@receiver(post_save, sender=DailyProgress)
def update_community_progress(sender, instance, **kwargs):
    BASE_API_URL = 'https://shadizargar.pythonanywhere.com/'  # آدرس پایه API خود را اینجا وارد کنید

    habit = instance.habit
    total_completed = sum(dp.completed_amount for dp in habit.daily_progress.all())
    progress_percentage = (total_completed / habit.goal) * 100 if habit.goal > 0 else 0

    habit.progress = progress_percentage
    habit.save()
    cache.set(f'habit_{habit.id}_progress', progress_percentage)

    # پیدا کردن درخواست عضویت مربوط به این عادت و کاربر
    membership_request = MembershipRequest.objects.filter(selected_habit=habit, requester=habit.user).first()
    community_id = membership_request.community.id if membership_request else None
    
    # ارسال درخواست به‌روزرسانی به کامیونیتی
    if community_id:
        update_progress_url = f'{BASE_API_URL}/api/community/communities/{community_id}/update_habit_progress/'
        data = {
            'habit_id': habit.id,
            'completed': instance.completed_amount > 0
        }
        try:
            response = requests.post(update_progress_url, json=data)
            response.raise_for_status()
            print("Community progress updated successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error updating community progress: {e}")
