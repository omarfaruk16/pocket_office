# forms.py

from django import forms
from django.contrib.auth.models import User
# from django.forms import modelformset_factory # Not strictly needed if not using formsets here
from .models import Teacher, Degree # Make sure both are imported

class TeacherRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    teacher_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Teacher's ID"}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}))
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Mobile Number'}))
    permanent_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Address'}))
    picture = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()

        # Password match check
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match")

        # Email uniqueness check
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already in use.")

        return cleaned_data

# Degree form
class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['degree_name', 'slug', 'university', 'passing_year', 'result']
        widgets = {
            'degree_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'passing_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'result': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Teacher form (original, specific to teacher_id and picture)
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'picture']


# Login form
class TeacherLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

# NEW: Teacher Profile Edit Form
class TeacherProfileForm(forms.ModelForm):
    # Add User model fields directly to the TeacherProfileForm
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})) # Username usually not editable

    class Meta:
        model = Teacher
        fields = ['phone', 'permanent_address', 'picture'] # Fields directly from Teacher model
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}), # For file uploads
        }

    def __init__(self, *args, **kwargs):
        # Populating initial data for User fields
        user_instance = kwargs.pop('user', None) # Get user instance from kwargs
        super().__init__(*args, **kwargs)

        if user_instance:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['email'].initial = user_instance.email
            self.fields['username'].initial = user_instance.username

        # Set placeholders for fields dynamically if needed, or remove if not desired
        # self.fields['phone'].widget.attrs['placeholder'] = 'Enter your phone number'
        # self.fields['permanent_address'].widget.attrs['placeholder'] = 'Enter your address'
        # self.fields['picture'].widget.attrs['placeholder'] = 'Upload new picture'


    def save(self, commit=True):
        teacher = super().save(commit=False)
        user = teacher.user # Get the related User instance

        # Update User fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # username is read-only, so no update needed here

        if commit:
            user.save()
            teacher.save()
        return teacher