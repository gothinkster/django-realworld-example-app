from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _

from symposion.reviews.models import Review, Comment, ProposalMessage, VOTES


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["vote", "comment"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["vote"] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=VOTES.CHOICES
        )


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class SpeakerCommentForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["message"]


class BulkPresentationForm(forms.Form):
    talk_ids = forms.CharField(
        label=_("Talk ids"),
        max_length=500,
        help_text=_("Provide a comma seperated list of talk ids to accept.")
    )
