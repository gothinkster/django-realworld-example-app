from __future__ import unicode_literals
from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(Speaker,
                    list_display=["name", "email", "created", "twitter_username"],
                    search_fields=["name"])
