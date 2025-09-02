from django.contrib import admin
from .models import Semester, Course, Part, Class, Attendance, CT, CTResult, Exam, ExamResult

    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credit', 'semester']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'teacher']
    
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['part', 'class_number', 'date', 'topic']
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['class_session', 'student', 'status']
    
@admin.register(CT)
class CTAdmin(admin.ModelAdmin):
    list_display = ['part', 'ct_number', 'date', 'topic', 'total_marks']
    
@admin.register(CTResult)
class CTResultAdmin(admin.ModelAdmin):
    list_display = ['ct', 'student', 'marks']
    
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['part', 'date', 'topic', 'total_marks']
    
@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['exam', 'student', 'marks']