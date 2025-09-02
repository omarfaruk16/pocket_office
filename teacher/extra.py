


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ['degree_name', 'teacher', 'university', 'passing_year', 'result']
    search_fields = ['degree_name', 'university', 'teacher__user__username']
    prepopulated_fields = {"slug": ("degree_name",)}