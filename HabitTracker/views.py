from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone  # Import timezone
from datetime import timedelta  # Import timedelta
from .models import Habit, DailyProgress
from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.response import Response


def habits_list_view(request):
    habits = Habit.objects.all()
    return render(request, 'HabitTracker/habits_list.html', {'habits': habits})

def habit_create_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        duration = int(request.POST['duration'])  # Get the duration from the form
        # Create a new habit with the given duration (no need for start/end date)
        Habit.objects.create(name=name, description=description, duration=duration)
        return redirect('habits-list')
    return render(request, 'HabitTracker/habit_create.html')


def habit_edit_view(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)
    if request.method == 'POST':
        habit.name = request.POST['name']
        habit.description = request.POST.get('description', '')
        habit.duration = int(request.POST['duration'])  # Update the duration
        habit.save()
        return redirect('habit-detail', habit_id=habit.id)
    
    return render(request, 'HabitTracker/habit_edit.html', {'habit': habit})


# views.py (habit_detail view already implemented above)
def habit_detail(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)

    # Default duration in case it is None
    if habit.duration is None:
        habit.duration = 30  # Default to 30 days

    today = timezone.now().date()
    start_date = today
    end_date = start_date + timedelta(days=habit.duration - 1)

    # Get the daily progress within the date range
    daily_progress = DailyProgress.objects.filter(habit=habit, date__range=[start_date, end_date])

    if request.method == 'POST':
        # Update daily progress based on the form data
        for progress in daily_progress:
            checkbox_name = f"day_{progress.date}"
            completed = checkbox_name in request.POST
            progress.completed = completed
            progress.save()

        # After updating, redirect back to the same habit detail page
        return HttpResponseRedirect(reverse('habit-detail', args=[habit_id]))

    # Calculate progress
    completed_days = daily_progress.filter(completed=True).count()
    progress_percentage = (completed_days / habit.duration) * 100

    return render(request, 'HabitTracker/habit_detail.html', {
        'habit': habit,
        'daily_progress': daily_progress,
        'progress_percentage': progress_percentage,
    })



def habit_reset_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    habit.progress = 0  # Assuming you are resetting progress here
    habit.save()
    return render(request, 'HabitTracker/habit_reset.html', {'habit': habit})

def habit_delete_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        habit.delete()
        return redirect('habits-list')  # Redirect to habit list view
    return render(request, 'HabitTracker/habit_detail.html', {'habit': habit})




class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # ذخیره کاربر وارد شده # به جای کاربر وارد شده، مقدار None را برای user ذخیره می‌کنیم

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class UserHabitViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user_habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(user_habits, many=True)
        return Response(serializer.data)