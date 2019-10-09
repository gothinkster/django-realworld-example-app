from __future__ import unicode_literals
from django import forms

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from symposion.teams.models import Membership


class TeamInvitationForm(forms.Form):

    email = forms.EmailField(label=_("Email"),
                             help_text=_("email address must be that of an account on this "
                                         "conference site"))

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInvitationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TeamInvitationForm, self).clean()
        email = cleaned_data.get("email")

        if email is None:
            raise forms.ValidationError(_("valid email address required"))

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # eventually we can invite them but for now assume they are
            # already on the site
            raise forms.ValidationError(
                mark_safe(_("no account with email address <b>%s</b> found on this conference "
                          "site") % escape(email)))

        state = self.team.get_state_for_user(user)

        if state in ["member", "manager"]:
            raise forms.ValidationError(_("user already in team"))

        if state in ["invited"]:
            raise forms.ValidationError(_("user already invited to team"))

        self.user = user
        self.state = state

        return cleaned_data

    def invite(self):
        if self.state is None:
            Membership.objects.create(team=self.team, user=self.user, state="invited")
        elif self.state == "applied":
            # if they applied we shortcut invitation process
            membership = Membership.objects.filter(team=self.team, user=self.user)
            membership.update(state="member")
