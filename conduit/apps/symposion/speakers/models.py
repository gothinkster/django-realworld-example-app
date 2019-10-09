from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from symposion.markdown_parser import parse


@python_2_unicode_compatible
class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]

    user = models.OneToOneField(User, null=True, related_name="speaker_profile", verbose_name=_("User"))
    name = models.CharField(verbose_name=_("Name"), max_length=100,
                            help_text=_("As you would like it to appear in the"
                                        " conference program."))
    biography = models.TextField(blank=True, help_text=_("A little bit about you.  Edit using "
                                                         "<a href='http://warpedvisions.org/projects/"
                                                         "markdown-cheat-sheet/target='_blank'>"
                                                         "Markdown</a>."), verbose_name=_("Biography"))
    biography_html = models.TextField(blank=True)
    photo = models.ImageField(upload_to="speaker_photos", blank=True, verbose_name=_("Photo"))
    twitter_username = models.CharField(
        max_length=15,
        blank=True,
        help_text=_(u"Your Twitter account")
    )
    annotation = models.TextField(verbose_name=_("Annotation"))  # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True, verbose_name=_("Invite_email"))
    invite_token = models.CharField(max_length=40, db_index=True, verbose_name=_("Invite token"))
    created = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        verbose_name=_("Created")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

    def save(self, *args, **kwargs):
        self.biography_html = parse(self.biography)
        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.name
        else:
            return "?"

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations
