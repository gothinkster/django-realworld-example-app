from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SponsorshipConfig(AppConfig):
    name = "symposion.sponsorship"
    label = "symposion_sponsorship"
    verbose_name = _("Symposion Sponsorship")
