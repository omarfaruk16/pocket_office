# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('remove/<int:student_id>/', views.remove_student, name='remove_student'),
    path('assign/<int:semester_id>/', views.assign_students, name='assign_students'),
]
