from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Industry, Skill, Job, JobType
from Employer.models import Employer
from Student.models import Student

class JobAdmin(admin.ModelAdmin):

    list_display = ('job_title', 'description', 'posted_by', 'salary_in_dhs', 'duration_in_months')
    list_display_links = ('job_title',)
    # list_editable = ('salary',)
    # list_filter = ('job_title', 'description')
    ordering = ['job_title']
    change_list_template = "admin/job_change_list.html"

    def salary_in_dhs(self, obj):
        return obj.salary

    def duration_in_months(self, obj):
        return obj.duration

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(Industry)
admin.site.register(Skill)