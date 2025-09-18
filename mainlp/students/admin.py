from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'institute', 'course', 'dormitory_number')
    list_filter = ('institute', 'course', 'dormitory_number', 'region')
    search_fields = ('full_name', 'phone', 'passport_data', 'city')
    date_hierarchy = 'created_at'