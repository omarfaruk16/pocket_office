from django import forms
from .models import Class, CT, Exam, Attendance, CTResult, ExamResult
from student.models import Student
from django.forms import formset_factory

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['date', 'topic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CTForm(forms.ModelForm):
    class Meta:
        model = CT
        fields = ['date', 'topic', 'total_marks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['date', 'topic', 'total_marks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class CTResultForm(forms.ModelForm):
    class Meta:
        model = CTResult
        fields = ['marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }