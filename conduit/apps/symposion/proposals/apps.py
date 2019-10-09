from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProposalsConfig(AppConfig):
    name = "symposion.proposals"
    label = "symposion_proposals"
    verbose_name = _("Symposion Proposals")
