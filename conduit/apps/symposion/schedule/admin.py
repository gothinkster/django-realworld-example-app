from __future__ import unicode_literals
from django.contrib import admin

from symposion.schedule.models import Schedule, Day, Room, SlotKind, Slot, SlotRoom, Presentation, Session, SessionRole


class DayInline(admin.StackedInline):
    model = Day
    extra = 2


class SlotKindInline(admin.StackedInline):
    model = SlotKind


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    inlines = [DayInline, SlotKindInline, ]


class SlotRoomInline(admin.TabularInline):
    model = SlotRoom
    extra = 1


class SlotAdmin(admin.ModelAdmin):
    list_filter = ("day", "kind")
    list_display = ("day", "start", "end", "kind", "content_override")
    inlines = [SlotRoomInline]


class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "schedule"]
    list_filter = ["schedule"]
    inlines = [SlotRoomInline]


class PresentationAdmin(admin.ModelAdmin):
    model = Presentation
    list_filter = ("section", "cancelled", "slot")


admin.site.register(Day)
admin.site.register(
    SlotKind,
    list_display=["label", "schedule"],
)
admin.site.register(
    SlotRoom,
    list_display=["slot", "room"]
)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Session)
admin.site.register(SessionRole)
admin.site.register(Presentation, PresentationAdmin)
