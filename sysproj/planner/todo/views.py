from django.shortcuts import render , redirect ,get_object_or_404
from django.http import JsonResponse
from .models import Task , ChecklistItem , Comment
from .forms import TaskForm , ChecklistItemForm ,CommentForm

from rest_framework import viewsets
from .serializers import TaskSerializer

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
            form.save()
            return redirect('index')
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