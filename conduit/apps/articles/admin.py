from django.contrib import admin
from conduit.apps.articles.models import Article, Tag

admin.site.register(Article)
admin.site.register(Tag)