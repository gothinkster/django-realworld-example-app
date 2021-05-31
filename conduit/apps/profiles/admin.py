from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'team']


admin.site.register(Profile, ProfileAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Team, TeamAdmin)