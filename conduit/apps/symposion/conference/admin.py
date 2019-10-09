from django.contrib import admin

from symposion.conference.models import Conference, Section


class SectionInline(admin.TabularInline):
    model = Section
    prepopulated_fields = {"slug": ("name",)}
    extra = 1


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date")
    inlines = [SectionInline, ]


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(
    Section,
    prepopulated_fields={"slug": ("name",)},
    list_display=("name", "conference", "start_date", "end_date")
)
