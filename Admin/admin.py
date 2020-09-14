from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django_comments.models import Comment

from .models import Admin

class adminAdmin(admin.ModelAdmin):
    change_list_template = "admin/admin_change_list.html"
    change_form_template = "admin/admin_change_form.html"

# Register your models here.
admin.site.register(Admin, adminAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
#admin.site.unregister(Site)
admin.site.unregister(Comment)
