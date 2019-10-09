from __future__ import unicode_literals
from django.conf.urls import url

from .views import (
    schedule_conference,
    schedule_edit,
    schedule_list,
    schedule_list_csv,
    schedule_presentation_detail,
    schedule_detail,
    schedule_slot_edit,
    schedule_json,
    session_staff_email,
    session_list,
    session_detail,
)

urlpatterns = [
    url(r"^$", schedule_conference, name="schedule_conference"),
    url(r"^edit/$", schedule_edit, name="schedule_edit"),
    url(r"^list/$", schedule_list, name="schedule_list"),
    url(r"^presentations.csv$", schedule_list_csv, name="schedule_list_csv"),
    url(r"^presentation/(\d+)/$", schedule_presentation_detail, name="schedule_presentation_detail"),
    url(r"^([\w\-]+)/$", schedule_detail, name="schedule_detail"),
    url(r"^([\w\-]+)/edit/$", schedule_edit, name="schedule_edit"),
    url(r"^([\w\-]+)/list/$", schedule_list, name="schedule_list"),
    url(r"^([\w\-]+)/presentations.csv$", schedule_list_csv, name="schedule_list_csv"),
    url(r"^([\w\-]+)/edit/slot/(\d+)/", schedule_slot_edit, name="schedule_slot_edit"),
    url(r"^conference.json", schedule_json, name="schedule_json"),
    url(r"^sessions/staff.txt$", session_staff_email, name="schedule_session_staff_email"),
    url(r"^sessions/$", session_list, name="schedule_session_list"),
    url(r"^session/(\d+)/$", session_detail, name="schedule_session_detail"),
]
