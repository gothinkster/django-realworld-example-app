from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SpeakersConfig(AppConfig):
    name = "symposion.speakers"
    label = "symposion_speakers"
    verbose_name = _("Symposion Speakers")
