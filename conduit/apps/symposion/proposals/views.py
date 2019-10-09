from __future__ import unicode_literals
import hashlib
import random
import sys

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import static

from django.contrib import messages
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from account.decorators import login_required
from account.models import EmailAddress

from symposion.proposals.models import (
    ProposalBase, ProposalSection, ProposalKind
)
from symposion.proposals.models import SupportingDocument, AdditionalSpeaker
from symposion.speakers.models import Speaker
from symposion.utils.mail import send_email

from symposion.proposals.forms import (
    AddSpeakerForm, SupportingDocumentCreateForm
)


def get_form(name):
    dot = name.rindex(".")
    mod_name, form_name = name[:dot], name[dot + 1:]
    __import__(mod_name)
    return getattr(sys.modules[mod_name], form_name)


def proposal_submit(request):
    if not request.user.is_authenticated():
        messages.info(request, _("To submit a proposal, please "
                                 "<a href='{0}'>log in</a> and create a speaker profile "
                                 "via the dashboard.".format(settings.LOGIN_URL)))
        return redirect("home")  # @@@ unauth'd speaker info page?
    else:
        try:
            request.user.speaker_profile
        except ObjectDoesNotExist:
            url = reverse("speaker_create")
            messages.info(request, _("To submit a proposal, first "
                                     "<a href='{0}'>create a speaker "
                                     "profile</a>.".format(url)))
            return redirect("dashboard")

    kinds = []
    for proposal_section in ProposalSection.available():
        for kind in proposal_section.section.proposal_kinds.all():
            kinds.append(kind)

    return render(request, "symposion/proposals/proposal_submit.html", {
        "kinds": kinds,
    })


def proposal_submit_kind(request, kind_slug):

    kind = get_object_or_404(ProposalKind, slug=kind_slug)

    if not request.user.is_authenticated():
        return redirect("home")  # @@@ unauth'd speaker info page?
    else:
        try:
            speaker_profile = request.user.speaker_profile
        except ObjectDoesNotExist:
            return redirect("dashboard")

    if not kind.section.proposalsection.is_available():
        return redirect("proposal_submit")

    form_class = get_form(settings.PROPOSAL_FORMS[kind_slug])

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.kind = kind
            proposal.speaker = speaker_profile
            proposal.save()
            form.save_m2m()
            messages.success(request, _("Proposal submitted."))
            if "add-speakers" in request.POST:
                return redirect("proposal_speaker_manage", proposal.pk)
            return redirect("dashboard")
    else:
        form = form_class()

    return render(request, "symposion/proposals/proposal_submit_kind.html", {
        "kind": kind,
        "proposal_form": form,
    })


@login_required
def proposal_speaker_manage(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.speaker != request.user.speaker_profile:
        raise Http404()

    if request.method == "POST":
        add_speaker_form = AddSpeakerForm(request.POST, proposal=proposal)
        if add_speaker_form.is_valid():
            message_ctx = {
                "proposal": proposal,
            }

            def create_speaker_token(email_address):
                # create token and look for an existing speaker to prevent
                # duplicate tokens and confusing the pending speaker
                try:
                    pending = Speaker.objects.get(
                        Q(user=None, invite_email=email_address)
                    )
                except Speaker.DoesNotExist:
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    token = hashlib.sha1(salt + email_address).hexdigest()
                    pending = Speaker.objects.create(
                        invite_email=email_address,
                        invite_token=token,
                    )
                else:
                    token = pending.invite_token
                return pending, token
            email_address = add_speaker_form.cleaned_data["email"]
            # check if email is on the site now
            users = EmailAddress.objects.get_users_for(email_address)
            if users:
                # should only be one since we enforce unique email
                user = users[0]
                message_ctx["user"] = user
                # look for speaker profile
                try:
                    speaker = user.speaker_profile
                except ObjectDoesNotExist:
                    speaker, token = create_speaker_token(email_address)
                    message_ctx["token"] = token
                    # fire off email to user to create profile
                    send_email(
                        [email_address], "speaker_no_profile",
                        context=message_ctx
                    )
                else:
                    # fire off email to user letting them they are loved.
                    send_email(
                        [email_address], "speaker_addition",
                        context=message_ctx
                    )
            else:
                speaker, token = create_speaker_token(email_address)
                message_ctx["token"] = token
                # fire off email letting user know about site and to create
                # account and speaker profile
                send_email(
                    [email_address], "speaker_invite",
                    context=message_ctx
                )
            invitation, created = AdditionalSpeaker.objects.get_or_create(
                proposalbase=proposal.proposalbase_ptr, speaker=speaker)
            messages.success(request, "Speaker invited to proposal.")
            return redirect("proposal_speaker_manage", proposal.pk)
    else:
        add_speaker_form = AddSpeakerForm(proposal=proposal)
    ctx = {
        "proposal": proposal,
        "speakers": proposal.speakers(),
        "add_speaker_form": add_speaker_form,
    }
    return render(request, "symposion/proposals/proposal_speaker_manage.html", ctx)


@login_required
def proposal_edit(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if request.user != proposal.speaker.user:
        raise Http404()

    if not proposal.can_edit():
        ctx = {
            "title": "Proposal editing closed",
            "body": "Proposal editing is closed for this session type."
        }
        return render(request, "symposion/proposals/proposal_error.html", ctx)

    form_class = get_form(settings.PROPOSAL_FORMS[proposal.kind.slug])

    if request.method == "POST":
        form = form_class(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            if hasattr(proposal, "reviews"):
                users = User.objects.filter(
                    Q(review__proposal=proposal) |
                    Q(proposalmessage__proposal=proposal)
                )
                users = users.exclude(id=request.user.id).distinct()
                for user in users:
                    ctx = {
                        "user": request.user,
                        "proposal": proposal,
                    }
                    send_email(
                        [user.email], "proposal_updated",
                        context=ctx
                    )
            messages.success(request, "Proposal updated.")
            return redirect("proposal_detail", proposal.pk)
    else:
        form = form_class(instance=proposal)

    return render(request, "symposion/proposals/proposal_edit.html", {
        "proposal": proposal,
        "form": form,
    })


@login_required
def proposal_detail(request, pk):
    queryset = ProposalBase.objects.select_related("speaker", "speaker__user")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if request.user not in [p.user for p in proposal.speakers()]:
        raise Http404()

    if "symposion.reviews" in settings.INSTALLED_APPS:
        from symposion.reviews.forms import SpeakerCommentForm
        message_form = SpeakerCommentForm()
        if request.method == "POST":
            message_form = SpeakerCommentForm(request.POST)
            if message_form.is_valid():

                message = message_form.save(commit=False)
                message.user = request.user
                message.proposal = proposal
                message.save()

                ProposalMessage = SpeakerCommentForm.Meta.model
                reviewers = User.objects.filter(
                    id__in=ProposalMessage.objects.filter(
                        proposal=proposal
                    ).exclude(
                        user=request.user
                    ).distinct().values_list("user", flat=True)
                )

                for reviewer in reviewers:
                    ctx = {
                        "proposal": proposal,
                        "message": message,
                        "reviewer": True,
                    }
                    send_email(
                        [reviewer.email], "proposal_new_message",
                        context=ctx
                    )

                return redirect(request.path)
        else:
            message_form = SpeakerCommentForm()
    else:
        message_form = None

    return render(request, "symposion/proposals/proposal_detail.html", {
        "proposal": proposal,
        "message_form": message_form
    })


@login_required
def proposal_cancel(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.speaker.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        proposal.cancelled = True
        proposal.save()
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "%s has been cancelled" % proposal.title)
        return redirect("dashboard")

    return render(request, "symposion/proposals/proposal_cancel.html", {
        "proposal": proposal,
    })


@login_required
def proposal_leave(request, pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    try:
        speaker = proposal.additional_speakers.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if request.method == "POST":
        proposal.additional_speakers.remove(speaker)
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "You are no longer speaking on %s" % proposal.title)
        return redirect("dashboard")
    ctx = {
        "proposal": proposal,
    }
    return render(request, "symposion/proposals/proposal_leave.html", ctx)


@login_required
def proposal_pending_join(request, pk):
    proposal = get_object_or_404(ProposalBase, pk=pk)
    speaking = get_object_or_404(AdditionalSpeaker, speaker=request.user.speaker_profile,
                                 proposalbase=proposal)
    if speaking.status == AdditionalSpeaker.SPEAKING_STATUS_PENDING:
        speaking.status = AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED
        speaking.save()
        messages.success(request, "You have accepted the invitation to join %s" % proposal.title)
        return redirect("dashboard")
    else:
        return redirect("dashboard")


@login_required
def proposal_pending_decline(request, pk):
    proposal = get_object_or_404(ProposalBase, pk=pk)
    speaking = get_object_or_404(AdditionalSpeaker, speaker=request.user.speaker_profile,
                                 proposalbase=proposal)
    if speaking.status == AdditionalSpeaker.SPEAKING_STATUS_PENDING:
        speaking.status = AdditionalSpeaker.SPEAKING_STATUS_DECLINED
        speaking.save()
        messages.success(request, "You have declined to speak on %s" % proposal.title)
        return redirect("dashboard")
    else:
        return redirect("dashboard")


@login_required
def document_create(request, proposal_pk):
    queryset = ProposalBase.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=proposal_pk)
    proposal = ProposalBase.objects.get_subclass(pk=proposal.pk)

    if proposal.cancelled:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = SupportingDocumentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.proposal = proposal
            document.uploaded_by = request.user
            document.save()
            return redirect("proposal_detail", proposal.pk)
    else:
        form = SupportingDocumentCreateForm()

    return render(request, "symposion/proposals/document_create.html", {
        "proposal": proposal,
        "form": form,
    })


@login_required
def document_download(request, pk, *args):
    document = get_object_or_404(SupportingDocument, pk=pk)
    if getattr(settings, "USE_X_ACCEL_REDIRECT", False):
        response = HttpResponse()
        response["X-Accel-Redirect"] = document.file.url
        # delete content-type to allow Gondor to determine the filetype and
        # we definitely don't want Django's crappy default :-)
        del response["content-type"]
    else:
        response = static.serve(request, document.file.name, document_root=settings.MEDIA_ROOT)
    return response


@login_required
def document_delete(request, pk):
    document = get_object_or_404(SupportingDocument, pk=pk, uploaded_by=request.user)
    proposal_pk = document.proposal.pk

    if request.method == "POST":
        document.delete()

    return redirect("proposal_detail", proposal_pk)
