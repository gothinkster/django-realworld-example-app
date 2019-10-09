from django.db import models


class SponsorManager(models.Manager):

    def active(self):
        return self.get_query_set().filter(active=True).order_by("level")
