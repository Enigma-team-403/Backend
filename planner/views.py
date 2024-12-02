from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, ChecklistItem, Comment
from .forms import TaskForm, ChecklistItemForm, CommentForm
from rest_framework import viewsets
from .serializers import TaskSerializer
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest
from .forms import TaskForm
from .models import Task



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

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'todo/add_task.html', {'form': form})
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})

def toggle_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'completed': task.completed})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            return redirect('task_detail', task_id=task_id)
    else:
        form = CommentForm()
    return render(request, 'todo/task_detail.html', {'task': task, 'comments': comments, 'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # Automatically mark the task as completed if the status is 'completed'
            if form.cleaned_data['status'] == 'completed':
                task.status = 'completed'
            form.save()
            return redirect('index')  # Redirect to the task list or appropriate page
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'deleted': True})

def change_priority(request, task_id, priority):
    task = get_object_or_404(Task, id=task_id)
    task.priority = priority
    task.save()
    return JsonResponse({'priority': task.priority})

def toggle_checklist_item_completed(request, item_id):
    item = get_object_or_404(ChecklistItem, id=item_id) 
    item.completed = not item.completed 
    item.save() 
    return redirect('index')


def delete_checklist_item(request, item_id): 
    item = get_object_or_404(ChecklistItem, id=item_id) 
    item.delete() 
    return JsonResponse({'status': 'success'})


def filter_tasks(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    tasks = Task.objects.all()

    if start_time and end_time:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
        tasks = tasks.filter(start_time__gte=start_time, end_time__lte=end_time)

    return JsonResponse({'tasks': list(tasks.values())})

def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'status': task.status})

def get_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return JsonResponse({'status': task.status})


def planner_view(request):
    planner_type = request.GET.get('planner_type', '3_days')  # Default to 3 days
    now = timezone.now()

    # Determine the end date for the selected planner type
    if planner_type == '3_days':
        end_date = now + timedelta(days=3)
    elif planner_type == 'weekly':
        end_date = now + timedelta(weeks=1)
    elif planner_type == 'monthly':
        end_date = now + timedelta(days=30)
    else:
        end_date = now + timedelta(days=3)  # Default to 3 days if invalid

    # Filter tasks whose `end_time` falls within the specified range
    tasks = Task.objects.filter(end_time__gte=now, end_time__lte=end_date)

    return render(request, 'todo/planner.html', {
        'tasks': tasks,
        'planner_type': planner_type,
    })


def planner_form_view(request):
    # Get the 'planner_type' and 'priority' from query parameters
    planner_type = request.GET.get('planner_type', '3_days')
    priority = request.GET.get('priority')  # Fetch priority from query params
    now = timezone.now()

    # Filter tasks based on the selected planner type
    if planner_type == '3_days':
        tasks = Task.objects.filter(start_time__gte=now, end_time__lte=now + timedelta(days=3))
    elif planner_type == 'weekly':
        tasks = Task.objects.filter(start_time__gte=now, end_time__lte=now + timedelta(weeks=1))
    elif planner_type == 'monthly':
        tasks = Task.objects.filter(start_time__gte=now, end_time__lte=now + timedelta(days=30))
    else:
        tasks = Task.objects.all()  # Default case: show all tasks

    # Apply priority filter if provided
    if priority:
        try:
            priority = int(priority)  # Convert priority to integer
            tasks = tasks.filter(priority=priority)
        except ValueError:
            pass  # Ignore invalid priority values

    return render(request, 'todo/planner_form.html', {'tasks': tasks, 'planner_type': planner_type, 'priority': priority})

