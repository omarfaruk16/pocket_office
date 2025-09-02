from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Todo # Ensure Todo is imported
from teacher.models import Teacher # Ensure Teacher is imported
from .forms import TodoForm
from django.core.paginator import Paginator
from django.utils import timezone # Import timezone for handling datetimes

class TodoDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'todos/todo_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, user=self.request.user)
        query = self.request.GET.get('q', '')
        all_todos = Todo.objects.filter(teacher=teacher, title__icontains=query).order_by('-created_at')
        paginator = Paginator(all_todos, 5)  # 5 per page
        page = self.request.GET.get('page')
        todos = paginator.get_page(page)
        context['todos'] = todos
        context['query'] = query
        return context

class TodoCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = TodoForm(request.POST)
        teacher = get_object_or_404(Teacher, user=request.user)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.teacher = teacher
            todo.save()
            return JsonResponse({"success": True, "message": "Todo created successfully."})
        # Return form errors if validation fails
        return JsonResponse({"success": False, "message": "Invalid form data.", "errors": form.errors}, status=400)

class TodoEditView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, teacher__user=request.user)
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Todo updated successfully."})
        # Return form errors if validation fails
        return JsonResponse({"success": False, "message": "Invalid form data.", "errors": form.errors}, status=400)

class TodoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, teacher__user=request.user)
        todo.delete()
        return JsonResponse({"success": True, "message": "Todo deleted successfully."})

class TodoToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, teacher__user=request.user)
        todo.is_completed = not todo.is_completed
        todo.save()
        return JsonResponse({"success": True, "completed": todo.is_completed, "message": "Task status updated."})

# New View to get details for editing
class TodoDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, teacher__user=request.user)

        # Format deadline for datetime-local input.
        # isoformat() handles timezone-aware datetimes well, and JavaScript's Date constructor
        # can parse it. The frontend JS will then format it correctly for the input type.
        formatted_deadline = None
        if todo.deadline:
            # Ensure the datetime is in the current timezone before formatting if necessary,
            # or simply use isoformat() which returns an ISO 8601 string including timezone if present.
            # The frontend JS will take care of converting this string to the format
            # expected by <input type="datetime-local">.
            formatted_deadline = todo.deadline.isoformat(timespec='minutes') # e.g., '2025-07-15T10:30' or '2025-07-15T10:30+06:00'


        data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'deadline': formatted_deadline, # Use the formatted string
            'is_completed': todo.is_completed,
        }
        return JsonResponse(data)

# TodoSearchView is not directly used by the edit flow, but keeping it
class TodoSearchView(LoginRequiredMixin, View):
    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)
        query = request.GET.get('q', '')
        # When returning JSON, you might want to serialize the deadline for consistency with TodoDetailView
        todos = Todo.objects.filter(teacher=teacher, title__icontains=query).values('id', 'title', 'description', 'is_completed')
        # Add formatted deadline to search results if needed for frontend display
        for todo_item in todos:
            todo_obj = Todo.objects.get(id=todo_item['id'])
            if todo_obj.deadline:
                todo_item['deadline'] = todo_obj.deadline.isoformat(timespec='minutes')
            else:
                todo_item['deadline'] = None
        return JsonResponse({"results": list(todos)})