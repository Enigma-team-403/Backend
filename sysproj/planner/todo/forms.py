from django import forms
from .models import Task , Comment
from .models import ChecklistItem

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'priority', 'color' , 'date', 'time', 'alarm_time']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}) ,
            'alarm_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['title', 'completed']
        widgets = { 'completed': forms.CheckboxInput(attrs={'class': 'checklist-checkbox'}), }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 40})
        }
