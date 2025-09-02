from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoDashboardView.as_view(), name='todo_dashboard'),
    path('todos/create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('todos/edit/<int:pk>/', views.TodoEditView.as_view(), name='todo_edit'),
    path('todos/delete/<int:pk>/', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('todos/toggle/<int:pk>/', views.TodoToggleView.as_view(), name='todo_toggle'),
    path('todos/detail/<int:pk>/', views.TodoDetailView.as_view(), name='todo_detail'), # <--- ADD THIS LINE
    # If you intend to use TodoSearchView for AJAX, you might need a URL for it too:
    # path('todos/search/', views.TodoSearchView.as_view(), name='todo_search'),
]