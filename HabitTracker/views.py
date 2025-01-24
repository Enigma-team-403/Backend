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
from .serializers import HabitSerializer,DailyProgressSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from community.models import MembershipRequest
import requests
from .models import DailyProgress
from .serializers import DailyProgressSerializer
from rest_framework import generics
from .models import Habit
from .serializers import HabitSerializer


class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

class HabitCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = HabitCreateSerializer(data=request.data)
        if serializer.is_valid():
            habit = serializer.save(user=request.user)  # اضافه کردن کاربر به عادت
            today = timezone.now().date()
            for i in range(habit.duration):
                progress_date = today + timedelta(days=i)
                DailyProgress.objects.create(habit=habit, date=progress_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitDeleteView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitUpdateView(APIView):
    def put(self, request, pk, format=None):
        habit = get_object_or_404(Habit, pk=pk)
        serializer = HabitSerializer(habit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.timezone import now

class UpdateProgressView(APIView):
    def post(self, request, format=None):
        habit_id = request.data.get('habit_id')
        completed = request.data.get('completed', False)  # مقدار پیش‌فرض False

        habit = get_object_or_404(Habit, id=habit_id)
        current_date = now().date()

        # بررسی وجود DailyProgress برای تاریخ جاری
        if DailyProgress.objects.filter(habit=habit, date=current_date).exists():
            return Response({'message': 'You have already done this habit today.', 'progress': habit.progress}, status=status.HTTP_400_BAD_REQUEST)

        # ایجاد DailyProgress برای تاریخ جاری
        daily_progress = DailyProgress.objects.create(habit=habit, date=current_date)

        if completed:
            daily_progress.completed_amount = habit.daily_target  # اگر انجام شد، مقدار daily_target اضافه شود
        else:
            daily_progress.completed_amount = 0  # اگر انجام نشد، مقدار صفر باشد
        
        daily_progress.save()

        # به‌روزرسانی پیشرفت عادت
        total_completed = sum(dp.completed_amount for dp in habit.daily_progress.all())
        habit.progress = (total_completed / habit.goal) * 100 if habit.goal > 0 else 0
        habit.save()

        message = "Today's habit is done." if completed else "Today's habit is not done."


        return Response({'message': message, 'progress': habit.progress}, status=status.HTTP_200_OK)






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


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            progress_id = data.get('progress_id')
            completed = data.get('completed')

            progress = DailyProgress.objects.get(id=progress_id)
            habit = progress.habit

            progress.completed = completed
            progress.save()

            completed_days = DailyProgress.objects.filter(habit=habit, completed=True).count()
            habit.progress = (completed_days / habit.duration) * 100 if habit.duration > 0 else 0
            habit.save()

            return JsonResponse({'success': True, 'progress': habit.progress})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def habit_create_view(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # اضافه کردن لاگ برای بررسی داده‌های POST
        name = request.POST.get('name')
        if not name:
            print("Name field is missing in the POST data")
            return JsonResponse({'error': 'Name field is required'}, status=400)
        description = request.POST.get('description', '')
        duration = int(request.POST.get('duration', 7))  # اضافه کردن مقدار پیش فرض برای duration
        print(f"Creating habit with name: {name}, description: {description}, duration: {duration}")
        habit = Habit.objects.create(name=name, description=description, duration=duration)
        today = timezone.now().date()
        for i in range(duration):
            progress_date = today + timedelta(days=i) 
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