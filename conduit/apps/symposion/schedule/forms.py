from __future__ import unicode_literals
import csv
import time

from datetime import datetime

from django import forms
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Q

from symposion.schedule.models import (Day, Presentation, Room, SlotKind, Slot,
                                       SlotRoom)


class SlotEditForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.slot = kwargs.pop("slot")
        super(SlotEditForm, self).__init__(*args, **kwargs)
        # @@@ TODO - Make this configurable
        if self.slot.kind.label in ["talk", "tutorial", "keynote"]:
            self.fields["presentation"] = self.build_presentation_field()
        else:
            self.fields["content_override"] = self.build_content_override_field()

    def build_presentation_field(self):
        kwargs = {}
        queryset = Presentation.objects.all()
        queryset = queryset.exclude(cancelled=True)
        queryset = queryset.order_by("proposal_base__pk")
        if self.slot.content:
            queryset = queryset.filter(Q(slot=None) | Q(pk=self.slot.content.pk))
            kwargs["required"] = False
            kwargs["initial"] = self.slot.content
        else:
            queryset = queryset.filter(slot=None)
            kwargs["required"] = True
        kwargs["queryset"] = queryset
        return forms.ModelChoiceField(**kwargs)

    def build_content_override_field(self):
        kwargs = {
            "label": "Content",
            "required": False,
            "initial": self.slot.content_override,
        }
        return forms.CharField(**kwargs)


class ScheduleSectionForm(forms.Form):
    ROOM_KEY = 'room'
    DATE_KEY = 'date'
    START_KEY = 'time_start'
    END_KEY = 'time_end'
    KIND = 'kind'

    filename = forms.FileField(
        label='Select a CSV file to import:',
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop("schedule")
        super(ScheduleSectionForm, self).__init__(*args, **kwargs)

    def clean_filename(self):
        if 'submit' in self.data:
            fname = self.cleaned_data.get('filename')
            if not fname or not fname.name.endswith('.csv'):
                raise forms.ValidationError(u'Please upload a .csv file')
            return fname

    def _get_start_end_times(self, data):
        "Return start and end time objects"
        times = []
        for x in [data[self.START_KEY], data[self.END_KEY]]:
            try:
                time_obj = time.strptime(x, '%I:%M %p')
            except:
                return messages.ERROR, u'Malformed time found: %s.' % x
            time_obj = datetime(100, 1, 1, time_obj.tm_hour, time_obj.tm_min, 00)
            times.append(time_obj.time())
        return times

    def _build_rooms(self, data):
        "Get or Create Rooms based on schedule type and set of Tracks"
        created_rooms = []
        rooms = sorted(set([x[self.ROOM_KEY] for x in data]))
        for i, room in enumerate(rooms):
            room, created = Room.objects.get_or_create(
                schedule=self.schedule, name=room, order=i
            )
            if created:
                created_rooms.append(room)
        return created_rooms

    def _build_days(self, data):
        "Get or Create Days based on schedule type and set of Days"
        created_days = []
        days = set([x[self.DATE_KEY] for x in data])
        for day in days:
            try:
                date = datetime.strptime(day, "%m/%d/%Y")
            except ValueError:
                [x.delete() for x in created_days]
                return messages.ERROR, u'Malformed data found: %s.' % day
            day, created = Day.objects.get_or_create(
                schedule=self.schedule, date=date
            )
            if created:
                created_days.append(day)
        return created_days

    def build_schedule(self):
        created_items = []
        reader = csv.DictReader(self.cleaned_data.get('filename'))
        data = [dict((k.strip(), v.strip()) for k, v in x.items()) for x in reader]
        # build rooms
        created_items.extend(self._build_rooms(data))
        # build_days
        created_items.extend(self._build_days(data))
        # build Slot  -> SlotRoom
        for row in data:
            room = Room.objects.get(
                schedule=self.schedule, name=row[self.ROOM_KEY]
            )
            date = datetime.strptime(row[self.DATE_KEY], "%m/%d/%Y")
            day = Day.objects.get(schedule=self.schedule, date=date)
            start, end = self._get_start_end_times(row)
            slot_kind, created = SlotKind.objects.get_or_create(
                label=row[self.KIND], schedule=self.schedule
            )
            if created:
                created_items.append(slot_kind)
            if row[self.KIND] == 'plenary':
                slot, created = Slot.objects.get_or_create(
                    kind=slot_kind, day=day, start=start, end=end
                )
                if created:
                    created_items.append(slot)
            else:
                slot = Slot.objects.create(
                    kind=slot_kind, day=day, start=start, end=end
                )
                created_items.append(slot)
            try:
                with transaction.atomic():
                    SlotRoom.objects.create(slot=slot, room=room)
            except IntegrityError:
                # delete all created objects and report error
                for x in created_items:
                    x.delete()
                return messages.ERROR, u'An overlap occurred; the import was cancelled.'
        return messages.SUCCESS, u'Your schedule has been imported.'

    def delete_schedule(self):
        self.schedule.day_set.all().delete()
        return messages.SUCCESS, u'Your schedule has been deleted.'
