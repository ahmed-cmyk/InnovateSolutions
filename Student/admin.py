from django.contrib import admin
from .models import Student, StudentJobApplication


class StudentList(admin.ModelAdmin):
    list_filter = ('is_active',)


# Register your models here.
admin.site.register(Student, StudentList)
