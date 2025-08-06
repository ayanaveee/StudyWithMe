from django import forms
from .models import StudySession, Goal

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['note']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }

