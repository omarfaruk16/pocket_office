from django.urls import path
from . import views

urlpatterns = [
     path('teacher/dashboard/', views.TeacherPartListView.as_view(), name='teacher_part_list'),
    # Part Page: Display Classes, CTs, Exams for a specific part
    path('part/<int:part_id>/', views.part_detail, name='part_detail'),
    path('part/<int:part_id>/create-class/', views.create_class, name='create_class'),
    path('part/<int:part_id>/create-ct/', views.create_ct, name='create_ct'),
    path('part/<int:part_id>/create-exam/', views.create_exam, name='create_exam'),
    path('class/<int:class_id>/edit/', views.edit_class, name='edit_class'),
    path('ct/<int:ct_id>/edit/', views.edit_ct, name='edit_ct'),
    path('exam/<int:exam_id>/edit/', views.edit_exam, name='edit_exam'),
    path('class/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('ct/<int:ct_id>/delete/', views.delete_ct, name='delete_ct'),
    path('exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),
]


