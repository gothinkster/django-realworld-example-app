"""
This file contains functions that are useful to humans at the shell for
manipulating the database in more natural ways.
"""
from __future__ import unicode_literals
from django.db import transaction

from .models import Schedule, Day, Room, Slot, SlotKind, SlotRoom


@transaction.commit_on_success
def create_slot(section_slug, date, kind, start, end, rooms):
    schedule = Schedule.objects.get(section__slug=section_slug)
    slot = Slot()
    slot.day = Day.objects.get(schedule=schedule, date=date)
    slot.kind = SlotKind.objects.get(schedule=schedule, label=kind)
    slot.start = start
    slot.end = end
    slot.save(force_insert=True)
    if rooms == "all":
        rooms_qs = Room.objects.filter(schedule=schedule).order_by("order")
    else:
        rooms_qs = Room.objects.filter(schedule=schedule, name__in=rooms).order_by("order")
        if rooms_qs.count() != len(rooms):
            raise Exception("input rooms do not match queried rooms; typo?")
    for room in rooms_qs:
        slot_room = SlotRoom()
        slot_room.slot = slot
        slot_room.room = room
        slot_room.save(force_insert=True)
    print "created {} [start={}; end={}]".format(slot.kind.label, slot.start, slot.end)
