from django.contrib import admin
from .models import *

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['user','bio']

admin.site.register(Profile, ProfilesAdmin)