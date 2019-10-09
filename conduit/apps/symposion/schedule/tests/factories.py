import datetime
import random

import factory

from factory import fuzzy

from symposion.schedule.models import Schedule, Day, Slot, SlotKind
from symposion.conference.models import Section, Conference


class ConferenceFactory(factory.DjangoModelFactory):
    title = fuzzy.FuzzyText()
    start_date = fuzzy.FuzzyDate(datetime.date(2014, 1, 1))
    end_date = fuzzy.FuzzyDate(
        datetime.date(2014, 1, 1) + datetime.timedelta(days=random.randint(1, 10))
    )
    # timezone = TimeZoneField("UTC")

    class Meta:
        model = Conference


class SectionFactory(factory.DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    name = fuzzy.FuzzyText()
    slug = fuzzy.FuzzyText()

    class Meta:
        model = Section


class ScheduleFactory(factory.DjangoModelFactory):
    section = factory.SubFactory(SectionFactory)
    published = True
    hidden = False

    class Meta:
        model = Schedule


class SlotKindFactory(factory.DjangoModelFactory):
    schedule = factory.SubFactory(ScheduleFactory)
    label = fuzzy.FuzzyText()

    class Meta:
        model = SlotKind


class DayFactory(factory.DjangoModelFactory):
    schedule = factory.SubFactory(ScheduleFactory)
    date = fuzzy.FuzzyDate(datetime.date(2014, 1, 1))

    class Meta:
        model = Day


class SlotFactory(factory.DjangoModelFactory):
    day = factory.SubFactory(DayFactory)
    kind = factory.SubFactory(SlotKindFactory)
    start = datetime.time(random.randint(0, 23), random.randint(0, 59))
    end = datetime.time(random.randint(0, 23), random.randint(0, 59))

    class Meta:
        model = Slot
