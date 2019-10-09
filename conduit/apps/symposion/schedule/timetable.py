from __future__ import unicode_literals
import itertools

from django.db.models import Count, Min

from symposion.schedule.models import Room, Slot, SlotRoom


class TimeTable(object):

    def __init__(self, day):
        self.day = day

    def slots_qs(self):
        qs = Slot.objects.all()
        qs = qs.filter(day=self.day)
        return qs

    def rooms(self):
        qs = Room.objects.all()
        qs = qs.filter(schedule=self.day.schedule)
        qs = qs.filter(
            pk__in=SlotRoom.objects.filter(slot__in=self.slots_qs().values("pk")).values("room"))
        qs = qs.order_by("order")
        return qs

    def __iter__(self):
        times = sorted(set(itertools.chain(*self.slots_qs().values_list("start", "end"))))
        slots = Slot.objects.filter(pk__in=self.slots_qs().values("pk"))
        slots = slots.annotate(room_count=Count("slotroom"), order=Min("slotroom__room__order"))
        slots = slots.order_by("start", "order")
        row = []
        for time, next_time in pairwise(times):
            row = {"time": time, "slots": []}
            for slot in slots:
                if slot.start == time:
                    slot.rowspan = TimeTable.rowspan(times, slot.start, slot.end)
                    slot.colspan = slot.room_count
                    row["slots"].append(slot)
            if row["slots"] or next_time is None:
                yield row

    @staticmethod
    def rowspan(times, start, end):
        return times.index(end) - times.index(start)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    b.next()
    return itertools.izip_longest(a, b)
