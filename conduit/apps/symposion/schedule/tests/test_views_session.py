from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from symposion.conference.models import Section, current_conference, Conference
from symposion.schedule.models import Day, Schedule, Session


class TestScheduleViews(TestCase):
    username = "user@example.com"
    first_name = "Sam"
    last_name = "McGillicuddy"

    def setUp(self):
        self.user = User.objects.create_user(self.username,
                                             password="pass",
                                             email=self.username)
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

    def test_session_list(self):
        # Really minimal test for session list
        rsp = self.client.get(reverse("schedule_session_list"))
        self.assertEqual(200, rsp.status_code)

    def test_session_staff_email(self):
        # login and staff required
        self.user.is_staff = True
        self.user.save()
        assert self.client.login(username=self.username, password="pass")

        url = reverse("schedule_session_staff_email")
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)

    def test_session_detail(self):
        # really minimal test
        Conference.objects.get_or_create(id=settings.CONFERENCE_ID)
        section = Section.objects.create(
            conference=current_conference(),
        )
        schedule = Schedule.objects.create(
            section=section,
        )
        day = Day.objects.create(
            schedule=schedule,
            date=date.today(),
        )
        session = Session.objects.create(
            day=day,
        )
        url = reverse("schedule_session_detail", args=(session.pk,))
        rsp = self.client.get(url)
        self.assertEqual(200, rsp.status_code)
