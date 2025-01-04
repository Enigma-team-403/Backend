from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone  # Import timezone
from datetime import timedelta  # Import timedelta
from django.utils.timezone import localtime
from .models import Habit, DailyProgress
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json



def habits_list_view(request):
    if request.method == 'POST':
        progress_id = request.POST.get('progress_id')

        if progress_id:
            try:
                progress = get_object_or_404(DailyProgress, id=progress_id)
                progress.completed = not progress.completed  # Toggle the completion status
                progress.save()
                return redirect('habits-list')  # Redirect back to avoid duplicate submissions
            except DailyProgress.DoesNotExist:
                return redirect('habits-list')
        else:
            return redirect('habits-list')

    # For GET requests, display the habits
    habits = Habit.objects.all()
    habits_with_progress = []

    for habit in habits:
        today = timezone.now().date()
        start_date = today
        end_date = today + timedelta(days=habit.duration - 1)

        # Filter or create DailyProgress records only within the habit's start and duration
        daily_progresses = []
        for single_date in (start_date + timedelta(days=n) for n in range(habit.duration)):
            progress, created = DailyProgress.objects.get_or_create(habit=habit, date=single_date)
            daily_progresses.append(progress)

        # Fetch all progress for rendering
        habits_with_progress.append({
            'habit': habit,
            'daily_progress': daily_progresses
        })

    return render(request, 'HabitTracker/habits_list.html', {'habits_with_progress': habits_with_progress})


def update_progress(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            progress_id = data.get('progress_id')
            completed = data.get('completed')

            # Fetch the daily progress entry
            progress = DailyProgress.objects.get(id=progress_id)
            habit = progress.habit

            # Update the completed status
            progress.completed = completed
            progress.save()

            # Recalculate the overall progress of the habit
            completed_days = DailyProgress.objects.filter(habit=habit, completed=True).count()
            habit.progress = (completed_days / habit.duration) * 100 if habit.duration > 0 else 0
            habit.save()

            # Return the updated progress percentage
            return JsonResponse({'success': True, 'progress': habit.progress})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def habit_create_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        duration = int(request.POST['duration'])

        # Create habit
        habit = Habit.objects.create(name=name, description=description, duration=duration)

        # Generate DailyProgress records starting from today (habit creation date)
        today = timezone.now().date()

        for i in range(duration):
            progress_date = today + timedelta(days=i)  # Starts from today and adds 0, 1, 2, etc.
            DailyProgress.objects.create(habit=habit, date=progress_date)

        return redirect('habits-list')
    
    return render(request, 'HabitTracker/habit_create.html')


def habit_detail(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)
    daily_progress = DailyProgress.objects.filter(habit=habit).order_by('date')

    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX requests for progress update
            date = request.POST.get('date')
            progress = DailyProgress.objects.filter(habit=habit, date=date).first()
            if progress:
                progress.completed = not progress.completed
                progress.save()

            completed_days = DailyProgress.objects.filter(habit=habit, completed=True).count()
            progress_percentage = (completed_days / habit.duration) * 100
            habit.progress = progress_percentage
            habit.save()

            return JsonResponse({'success': True, 'progress': progress_percentage})
        else:
            # Handle non-AJAX form submission for "Topic" and "Section"
            topic = request.POST.get('topic')
            section = request.POST.get('section')
            if topic:
                habit.topic = topic
            if section:
                habit.section = section
            habit.save()

    # Calculate progress
    completed_days = daily_progress.filter(completed=True).count()
    progress_percentage = (completed_days / habit.duration) * 100

    return render(request, 'HabitTracker/habit_detail.html', {
        'habit': habit,
        'daily_progress': daily_progress,
        'progress_percentage': progress_percentage,
        'sections': ['Morning', 'Afternoon', 'Night', 'Others'],  # Pass available sections
    })



def habit_edit_view(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id)
    
    if request.method == 'POST':
        # Update habit fields from the form
        habit.name = request.POST['name']
        habit.description = request.POST.get('description', '')
        new_duration = int(request.POST.get('duration', habit.duration))

        # Check if the duration has changed
        if new_duration != habit.duration:
            habit.duration = new_duration

            # Adjust DailyProgress records based on new duration
            today = timezone.now().date()
            current_progress_dates = DailyProgress.objects.filter(habit=habit).values_list('date', flat=True)

            # Generate dates based on the new duration
            new_progress_dates = [
                today + timedelta(days=i) for i in range(new_duration)
            ]

            # Add missing DailyProgress records
            for date in new_progress_dates:
                if date not in current_progress_dates:
                    DailyProgress.objects.create(habit=habit, date=date)

            # Remove extra DailyProgress records
            for date in current_progress_dates:
                if date not in new_progress_dates:
                    DailyProgress.objects.filter(habit=habit, date=date).delete()

        # Save updated habit
        habit.save()
        
        return redirect('habit-detail', habit_id=habit.id)

    return render(request, 'HabitTracker/habit_edit.html', {'habit': habit})

def habit_reset_view(request, habit_id):
    # Fetch the habit using the passed habit_id
    habit = get_object_or_404(Habit, pk=habit_id)

    # Reset all daily progress entries for this habit
    habit.daily_progress.update(completed=False)

    # Recalculate the overall progress as 0% since everything is unchecked
    habit.progress = 0
    habit.save()

    # Return a JsonResponse to indicate success
    return render(request, 'HabitTracker/habit_reset.html', {'habit': habit})
    # return JsonResponse({'success': True, 'message': 'Habit reset successfully.'})

def habit_delete_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    if request.method == 'POST':
        habit.delete()
        return redirect('habits-list')  # Redirect to habit list view after deletion

    # If the request method is not POST, you can render a confirmation page (optional)
    return render(request, 'HabitTracker/habit_delete.html', {'habit': habit})