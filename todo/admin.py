from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at','deadline', 'is_completed',)
    search_fields = ('title', 'created_at','deadline', 'is_completed',)
    list_filter = ('title', 'created_at','deadline', 'is_completed',)
# Re
