from django.contrib import admin

# Register your models here.
from .models import Alumni


class AlumniList(admin.ModelAdmin):
    list_filter = ('is_active',)


admin.site.register(Alumni, AlumniList)
