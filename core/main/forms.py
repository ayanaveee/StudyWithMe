from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'category', 'deadline', 'priority']
        widgets = {
            'title': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опиши свою цель...',
                'rows': 2
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
