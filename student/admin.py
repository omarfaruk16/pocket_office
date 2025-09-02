from django.contrib import admin
from .models import Semester, Student  

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name',]
    list_filter = ['name',]
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = ['name',]
    list_filter = ['name',]