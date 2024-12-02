from django import forms
from .models import Task , Comment
from .models import ChecklistItem

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'start_time', 'end_time', 'completed']
        widgets = {
            'priority': forms.Select(choices=[(i, str(i)) for i in range(1, 6)])  # Limit to values 1-5
        }

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        if priority < 1 or priority > 5:
            raise forms.ValidationError("Priority must be between 1 and 5.")
        return priority


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




