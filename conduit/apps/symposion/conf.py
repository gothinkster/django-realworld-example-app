from django.conf import settings  # noqa

from appconf import AppConf


class SymposionAppConf(AppConf):

    VOTE_THRESHOLD = 3
