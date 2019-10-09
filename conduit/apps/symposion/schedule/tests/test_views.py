import json

from django.test.client import Client
from django.test import TestCase

from . import factories


class ScheduleViewTests(TestCase):

    def test_empty_json(self):
        c = Client()
        r = c.get('/conference.json')
        assert r.status_code == 200

        conference = json.loads(r.content)
        assert 'schedule' in conference
        assert len(conference['schedule']) == 0

    def test_populated_empty_presentations(self):

        factories.SlotFactory.create_batch(size=5)

        c = Client()
        r = c.get('/conference.json')
        assert r.status_code == 200

        conference = json.loads(r.content)
        assert 'schedule' in conference
        assert len(conference['schedule']) == 5
