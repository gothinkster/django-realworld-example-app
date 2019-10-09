import os

from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from symposion.conference.models import Conference, Section

from ..forms import ScheduleSectionForm
from ..models import Day, Room, Schedule, Slot, SlotKind

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class ScheduleSectionFormTests(TestCase):

    def setUp(self):
        self.conference = Conference.objects.create(title='test')
        self.section = Section.objects.create(
            conference=self.conference,
            name='test')
        self.schedule = Schedule.objects.create(section=self.section)
        self.today = datetime.now()
        self.tomorrow = self.today + timedelta(days=1)

    def test_clean_filename(self):
        """Ensure a file is provided if the submit action was utilized"""
        data = {'submit': 'Submit'}
        form = ScheduleSectionForm(data=data, schedule=self.schedule)
        self.assertIn('filename', form.errors)

    def test_clean_filename_not_required(self):
        """Ensure file is not required if the delete action was utilize"""
        data = {'delete': 'Delete'}
        form = ScheduleSectionForm(data=data, schedule=self.schedule)
        self.assertTrue(form.is_valid())

    def test_delete(self):
        """Delete schedule (Days) for supplied section"""
        Day.objects.create(schedule=self.schedule, date=self.today)
        Day.objects.create(schedule=self.schedule, date=self.tomorrow)
        other_section = Section.objects.create(conference=self.conference, name='other')
        other_schedule = Schedule.objects.create(section=other_section)
        other_day = Day.objects.create(schedule=other_schedule, date=self.tomorrow)
        self.assertEqual(3, Day.objects.all().count())
        data = {'delete': 'Delete'}
        form = ScheduleSectionForm(data=data, schedule=self.schedule)
        form.delete_schedule()
        days = Day.objects.all()
        self.assertEqual(1, days.count())
        self.assertIn(other_day, days)

    def test_build_days(self):
        """Test private method to build days based off ingested CSV"""
        form = ScheduleSectionForm(schedule=self.schedule)
        data = (
            {'date': datetime.strftime(self.today, "%m/%d/%Y")},
            {'date': datetime.strftime(self.today, "%m/%d/%Y")},
            {'date': datetime.strftime(self.tomorrow, "%m/%d/%Y")},
        )
        self.assertEqual(0, Day.objects.all().count())
        form._build_days(data)
        self.assertEqual(2, Day.objects.all().count())

    def test_build_days_malformed(self):
        """Test failure for malformed date in CSV"""
        form = ScheduleSectionForm(schedule=self.schedule)
        data = (
            {'date': datetime.strftime(self.today, "%m/%d/%Y")},
            {'date': '12-12-12'}
        )
        self.assertEqual(0, Day.objects.all().count())
        msg_type, msg = form._build_days(data)
        self.assertEqual(0, Day.objects.all().count())
        self.assertEqual(40, msg_type)
        self.assertIn('12-12-12', msg)

    def test_build_rooms(self):
        """Test private method to build rooms based off ingested CSV"""
        form = ScheduleSectionForm(schedule=self.schedule)
        data = (
            {'room': 'foo'},
            {'room': 'bar'},
            {'room': 'foo'},
        )
        self.assertEqual(0, Room.objects.all().count())
        form._build_rooms(data)
        self.assertEqual(2, Room.objects.all().count())

    def test_get_start_end_times(self):
        """
        Test private method to convert start and end times based off
        ingested CSV
        """
        form = ScheduleSectionForm(schedule=self.schedule)
        start = '12:00 PM'
        end = '01:00 PM'
        data = {'time_start': start, 'time_end': end}
        start_time, end_time = form._get_start_end_times(data)
        self.assertEqual(start, start_time.strftime('%I:%M %p'))
        self.assertEqual(end, end_time.strftime('%I:%M %p'))

    def test_get_start_end_times_malformed(self):
        """
        Test private method for malformed time based off ingested CSV
        """
        form = ScheduleSectionForm(schedule=self.schedule)
        start = '12:00'
        end = '01:00'
        data = {'time_start': start, 'time_end': end}
        msg_type, msg = form._get_start_end_times(data)
        self.assertEqual(40, msg_type)
        self.assertIn('Malformed', msg)

    def test_build_schedule(self):
        """
        Test successful schedule build based off ingested CSV
        """
        self.assertEqual(0, Day.objects.all().count())
        self.assertEqual(0, Room.objects.all().count())
        self.assertEqual(0, Slot.objects.all().count())
        self.assertEqual(0, SlotKind.objects.all().count())
        schedule_csv = open(os.path.join(DATA_DIR, 'schedule.csv'), 'rb')
        file_data = {'filename': SimpleUploadedFile(schedule_csv.name, schedule_csv.read())}
        data = {'submit': 'Submit'}
        form = ScheduleSectionForm(data, file_data, schedule=self.schedule)
        form.is_valid()
        msg_type, msg = form.build_schedule()
        self.assertEqual(25, msg_type)
        self.assertIn('imported', msg)
        self.assertEqual(2, Day.objects.all().count())
        self.assertEqual(2, Room.objects.all().count())
        self.assertEqual(8, Slot.objects.all().count())
        self.assertEqual(2, SlotKind.objects.all().count())

    def test_build_schedule_overlap(self):
        """
        Test rolledback schedule build based off ingested CSV with Slot overlap
        """
        self.assertEqual(0, Day.objects.all().count())
        self.assertEqual(0, Room.objects.all().count())
        self.assertEqual(0, Slot.objects.all().count())
        self.assertEqual(0, SlotKind.objects.all().count())
        schedule_csv = open(os.path.join(DATA_DIR, 'schedule_overlap.csv'), 'rb')
        file_data = {'filename': SimpleUploadedFile(schedule_csv.name, schedule_csv.read())}
        data = {'submit': 'Submit'}
        form = ScheduleSectionForm(data, file_data, schedule=self.schedule)
        form.is_valid()
        msg_type, msg = form.build_schedule()
        self.assertEqual(40, msg_type)
        self.assertIn('overlap', msg)
        self.assertEqual(0, Day.objects.all().count())
        self.assertEqual(0, Room.objects.all().count())
        self.assertEqual(0, Slot.objects.all().count())
        self.assertEqual(0, SlotKind.objects.all().count())
