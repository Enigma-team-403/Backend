from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, ChecklistItem, Comment
from .forms import TaskForm, ChecklistItemForm, CommentForm
from rest_framework import viewsets
from .serializers import TaskSerializer
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .models import ChecklistItem



def get_checklist_items(request, task_id):
    checklist_items = ChecklistItem.objects.filter(task_id=task_id).values('id', 'title', 'completed')
    return JsonResponse({'checklist_items': list(checklist_items)})
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('priority')
    serializer_class = TaskSerializer

def index(request):
    tasks = Task.objects.all().order_by('priority')
    checklist_items = ChecklistItem.objects.all()
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ChecklistItemForm()
    return render(request, 'todo/index.html', {'tasks': tasks, 'checklist_items': checklist_items, 'form': form})


def change_priority(request, task_id, priority):
    task = get_object_or_404(Task, id=task_id)
    task.priority = priority
    task.save()
    return redirect('index')  # Redirect to the task list to reflect the updated priority


from django.http import JsonResponse

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an AJAX/API request
                return JsonResponse({
                    'status': 'success',
                    'task': {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': task.priority,
                        'start_time': task.start_time,
                        'end_time': task.end_time,
                        'completed': task.completed,
                    }
                })
            else:
                return redirect('index')  # Redirect for browser requests
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            else:
                return render(request, 'todo/add_task.html', {'form': form})
    else:
        form = TaskForm()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'GET requests are not allowed'}, status=405)
        else:
            return render(request, 'todo/add_task.html', {'form': form})


from django.http import JsonResponse

def toggle_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an API request
        return JsonResponse({'completed': task.completed})
    else:
        return redirect('index')  # Redirect for browser requests

import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task, Comment
from .forms import CommentForm

logger = logging.getLogger(__name__)

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()

    # Debug: Log the headers and request type
    logger.debug(f"Request headers: {request.headers}")
    logger.debug(f"Is AJAX request: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")

    if request.method == 'POST':
        # Handle JSON payload for API requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)  # Parse JSON payload
                form = CommentForm(data)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)
        else:
            # Handle form data for browser requests
            form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'comment': {
                        'id': comment.id,
                        'content': comment.content,
                        'created_at': comment.created_at
                    }
                })
            else:
                return redirect('task_detail', task_id=task_id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            else:
                return render(request, 'todo/task_detail.html', {'task': task, 'comments': comments, 'form': form})
    else:
        form = CommentForm()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'GET requests are not allowed'}, status=405)
        else:
            return render(request, 'todo/task_detail.html', {'task': task, 'comments': comments, 'form': form})



import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Handle JSON payload for API requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)  # Parse JSON payload
                form = TaskForm(data, instance=task)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)
        else:
            # Handle form data for browser requests
            form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'task': {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'priority': task.priority,
                        'start_time': task.start_time,
                        'end_time': task.end_time,
                        'completed': task.completed,
                    }
                })
            else:
                messages.success(request, 'Task updated successfully!')
                return redirect('index')  # Redirect for browser requests
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            else:
                messages.error(request, 'There were some errors with your form submission.')
                return render(request, 'todo/edit_task.html', {'form': form, 'task': task})
    else:
        form = TaskForm(instance=task)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'GET requests are not allowed'}, status=405)
        else:
            return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

from django.http import JsonResponse

def delete_task(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        task.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an API request
            return JsonResponse({'status': 'success', 'message': f'Task {task_id} successfully deleted.'})
        else:
            messages.success(request, f'Task {task_id} successfully deleted.')
            return redirect('index')  # Redirect for browser requests
    except Task.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': f'Task with ID {task_id} does not exist.'}, status=404)
        else:
            messages.error(request, f'Task with ID {task_id} does not exist.')
            return redirect('index')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Task, ChecklistItem

def toggle_checklist_item_completed(request, task_id, item_id):
    # Get the task and checklist item
    task = get_object_or_404(Task, id=task_id)
    item = get_object_or_404(ChecklistItem, id=item_id, task=task)  # Ensure the item belongs to the task

    # Toggle the completed status
    item.completed = not item.completed
    item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an API request
        return JsonResponse({'completed': item.completed})
    else:
        return redirect('index')  # Redirect for browser requests


def delete_checklist_item(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id)
    item.delete()
    return JsonResponse({'status': 'success'})


def filter_tasks(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    tasks = Task.objects.all()

    if start_time and end_time:
        try:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            tasks = tasks.filter(start_time__gte=start_time, end_time__lte=end_time)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

    return JsonResponse({'tasks': list(tasks.values())})


def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'status': task.status})


def get_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse({'status': task.status})

from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

def planner_view(request):
    planner_type = request.GET.get('planner_type', '3_days')  # Default to 3 days
    now = timezone.now()

    # Determine the start and end date for the selected planner type
    if planner_type == '3_days':
        end_date = now + timedelta(days=3)  # 3 days from now
    elif planner_type == 'weekly':
        end_date = now + timedelta(weeks=1)  # 1 week from now
    elif planner_type == 'monthly':
        end_date = now + timedelta(days=30)  # 30 days from now
    else:
        end_date = now + timedelta(days=3)  # Default to 3 days if invalid

    # Filter tasks based on the selected planner type
    tasks = Task.objects.filter(
        Q(end_time__gte=now, end_time__lte=end_date)  # Tasks that have an end time within the filter window
    ).values('id', 'title', 'description', 'priority', 'start_time', 'end_time', 'completed', 'status')

    # Return JSON response
    return JsonResponse({
        'planner_type': planner_type,
        'tasks': list(tasks)
    })

from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

def planner_form_view(request):
    planner_type = request.GET.get('planner_type', '3_days')
    now = timezone.now()

    # Determine the end date for the selected planner type
    if planner_type == '3_days':
        end_date = now + timedelta(days=3)  # 3 days from now
    elif planner_type == 'weekly':
        end_date = now + timedelta(weeks=1)  # 1 week from now
    elif planner_type == 'monthly':
        end_date = now + timedelta(days=30)  # 30 days from now
    else:
        end_date = now + timedelta(days=3)  # Default to 3 days if invalid

    # Filter tasks based on the selected planner type
    tasks = Task.objects.filter(
        Q(end_time__gte=now, end_time__lte=end_date)  # Tasks that have an end time within the filter window
    ).values('id', 'title', 'description', 'priority', 'start_time', 'end_time', 'completed', 'status')

    # Debugging: print tasks to check the filtering results
    print(f"Tasks found: {tasks}")

    # Return JSON response
    return JsonResponse({
        'planner_type': planner_type,
        'tasks': list(tasks)
    })