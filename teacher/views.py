from django.shortcuts import render, redirect
from .forms import TeacherForm,  TeacherLoginForm, DegreeForm, TeacherRegistrationForm
from .models import Teacher, Degree
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
# views.py
from .forms import (
    TeacherRegistrationForm,
    TeacherLoginForm,
    TeacherProfileForm, # NEWLY ADDED
    DegreeForm
)

# Teacher Registration View
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            # Create Teacher profile
            teacher = Teacher.objects.create(
                user=user,
                teacher_id=form.cleaned_data['teacher_id'],
                phone=form.cleaned_data['phone'],
                permanent_address=form.cleaned_data['permanent_address'],
                picture=form.cleaned_data['picture']
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('teacher_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'teacher_register.html', {'form': form})


# Teacher Login View
class TeacherLoginView(View):
    template_name = 'teacher_login.html'
    
    def get(self, request):
        form = TeacherLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('teacher_profile')
                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email.')

        return render(request, self.template_name, {'form': form})

class TeacherLogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('teacher_login')


# Teacher List View (assuming this exists for admin or other purposes)
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


# UPDATED: Teacher Profile View
class TeacherProfileView(LoginRequiredMixin, View):
    template_name = 'teacher_profile.html'

    def get(self, request, *args, **kwargs):
        try:
            teacher_profile = request.user.teacher
        except Teacher.DoesNotExist:
            teacher_profile = None # Consider redirecting to a page to create profile or show error

        form = TeacherProfileForm(instance=teacher_profile, user=request.user)

        context = {
            'teacher': teacher_profile,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            teacher_profile = request.user.teacher
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher profile not found. Please create one.')
            return redirect('teacher_profile') # Or a create profile view

        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('teacher_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            context = {
                'teacher': teacher_profile,
                'form': form,
            }
            return render(request, self.template_name, context)


# Degree Views (from previous interaction, with AJAX improvements)
@login_required
def degree_list_view(request):
    teacher = request.user.teacher
    degrees = Degree.objects.filter(teacher=teacher).order_by('passing_year')
    form = DegreeForm() # An empty form for the 'NEW +' modal
    return render(request, 'degree_list.html', {'degrees': degrees, 'form': form})

@login_required
@require_POST # Ensure this view only accepts POST requests
def degree_create_view(request):
    form = DegreeForm(request.POST)
    if form.is_valid():
        degree = form.save(commit=False)
        degree.teacher = request.user.teacher
        degree.save()
        # For AJAX, return a success JSON response instead of redirecting immediately
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': # Detect AJAX
             return JsonResponse({'success': True, 'message': 'Degree added successfully!'})
        return redirect('degree_list') # Fallback for non-AJAX or direct access
    else:
        # If form is invalid, return JSON errors for AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = dict(form.errors) # Convert error messages to a dict
            return JsonResponse({'success': False, 'errors': errors}, status=400) # 400 Bad Request
        # Fallback for non-AJAX POST request with invalid form: re-render the list page with form
        messages.error(request, 'Error creating degree. Please check the form.')
        return redirect('degree_list') # Or render with errors more explicitly

@login_required
@require_POST # Ensure this view only accepts POST requests
def degree_edit_view(request, pk):
    degree = get_object_or_404(Degree, pk=pk, teacher=request.user.teacher)
    form = DegreeForm(request.POST, instance=degree)
    if form.is_valid():
        form.save()
        # For AJAX, return success JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Degree updated successfully!'})
        return redirect('degree_list') # Fallback
    else:
        # If invalid, return JSON errors
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = dict(form.errors)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        messages.error(request, 'Error editing degree. Please check the form.')
        return redirect('degree_list') # Fallback


@login_required
@require_POST # Ensure this view only accepts POST requests
def degree_delete_view(request, pk):
    degree = get_object_or_404(Degree, pk=pk, teacher=request.user.teacher)
    degree.delete()
    # For AJAX, return success JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Degree deleted successfully!'})
    messages.success(request, 'Degree deleted successfully.')
    return redirect('degree_list') # Fallback


@login_required
@require_GET # Ensure this view only accepts GET requests
def degree_detail_api(request, pk):
    degree = get_object_or_404(Degree, pk=pk, teacher=request.user.teacher)
    data = {
        'id': degree.pk,
        'degree_name': degree.degree_name,
        'slug': degree.slug,
        'university': degree.university,
        'passing_year': degree.passing_year.isoformat() if degree.passing_year else '', # YYYY-MM-DD
        'result': degree.result,
    }
    return JsonResponse(data)

