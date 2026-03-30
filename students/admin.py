from django.contrib import admin
from .models import Class, Student

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Student)