from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Industry, Skill, Job, JobType, Major
from Employer.models import Employer
from Student.models import Student


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'date_posted', 'posted_by', 'salary_min', 'salary_max', 'duration_in_months')
    list_display_links = ('job_title',)
    # list_editable = ('salary',)
    list_filter = ('date_posted', 'status', 'location', 'job_type_id', 'industry_id', 'is_active')
    ordering = ['job_title']
    change_list_template = "Admin/job_change_list.html"

    def minimum_salary(self, obj):
        return obj.salary_min

    def maximum_salary(self, obj):
        return obj.salary_max

    def duration_in_months(self, obj):
        return obj.duration


# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(Industry)
admin.site.register(Skill)
admin.site.register(Major)
