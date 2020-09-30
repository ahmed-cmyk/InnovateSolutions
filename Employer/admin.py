from django.contrib import admin
from .models import Employer


class EmployerList(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'is_active')
    list_display_links = ('company_name',)
    list_filter = ('is_active',)
    ordering = ['company_name']
    change_list_template = "admin/view_employer.html"


# Register your models here.
admin.site.register(Employer, EmployerList)
