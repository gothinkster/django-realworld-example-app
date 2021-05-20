from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'description']


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['author', 'body']
    list_display = ['author', 'body']


admin.site.register(Comment, CommentAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'slug']


admin.site.register(Tag, TagAdmin)