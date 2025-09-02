from django.contrib import admin
from .models import Teacher, Degree


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'teacher_id', 'picture']
    search_fields = ['user__username', 'teacher_id']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ['degree_name', 'teacher', 'university', 'passing_year', 'result']
    search_fields = ['degree_name', 'university', 'teacher__user__username']
    prepopulated_fields = {"slug": ("degree_name",)}