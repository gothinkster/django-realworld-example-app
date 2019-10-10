from django.core.mail import send_mass_mail
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.views.decorators.http import require_POST

from account.decorators import login_required

# @@@ switch to pinax-teams
from symposion.teams.models import Team

from symposion.conf import settings
from symposion.proposals.models import ProposalBase, ProposalSection
from symposion.utils.mail import send_email

from symposion.reviews.forms import ReviewForm, SpeakerCommentForm
from symposion.reviews.forms import BulkPresentationForm
from symposion.reviews.forms import StaffCommentForm
from symposion.reviews.models import (
    ReviewAssignment, Review, LatestVote, ProposalResult, NotificationTemplate,
    ResultNotification
)


def proposals_generator(request, queryset, user_pk=None, check_speaker=True):

    for obj in queryset:
        # @@@ this sucks; we can do better
        if check_speaker:
            if request.user in [s.user for s in obj.speakers()]:
                continue

        try:
            obj.result
        except ProposalResult.DoesNotExist:
            ProposalResult.objects.get_or_create(proposal=obj)

        obj.comment_count = obj.result.comment_count
        obj.total_votes = obj.result.vote_count
        obj.plus_one = obj.result.plus_one
        obj.plus_zero = obj.result.plus_zero
        obj.minus_zero = obj.result.minus_zero
        obj.minus_one = obj.result.minus_one
        lookup_params = dict(proposal=obj)

        if user_pk:
            lookup_params["user__pk"] = user_pk
        else:
            lookup_params["user"] = request.user

        try:
            obj.user_vote = LatestVote.objects.get(**lookup_params).vote
            obj.user_vote_css = LatestVote.objects.get(**lookup_params).css_class()
        except LatestVote.DoesNotExist:
            obj.user_vote = None
            obj.user_vote_css = "no-vote"

        yield obj

def access_not_permitted(request,error_message):
    return render(request, "symposion/reviews/access_not_permitted.html", error_message)


# Returns a list of all proposals, proposals reviewed by the user, or the proposals the user has
# yet to review depending on the link user clicks in dashboard
@login_required
def review_section(request_review, section_slug, assigned=False, reviewed="all"):

    if not request_review.user.has_perm("reviews.can_review_%s" % section_slug):
        return render(request_review, "symposion/reviews/access_not_permitted.html", "you do not have access to reviews")

    section = get_object_or_404(ProposalSection, section__slug=section_slug)
    queryset = ProposalBase.objects.filter(kind__section=section.section)

    if assigned:
        assignments = ReviewAssignment.objects.filter(user=request_review.user)\
            .values_list("proposal__id")
        queryset = queryset.filter(id__in=assignments)

    # passing reviewed in from reviews.urls and out to review_list for
    # appropriate template header rendering
    if reviewed == "all":
        queryset = queryset.select_related("result").select_subclasses()
        reviewed = "all_reviews"
    elif reviewed == "reviewed":
        queryset = queryset.filter(reviews__user=request_review.user)
        reviewed = "user_reviewed"
    else:
        queryset = queryset.exclude(reviews__user=request_review.user).exclude(
            speaker__user=request_review.user)
        reviewed = "user_not_reviewed"

    proposals = proposals_generator(request_review, queryset)

    ctx = {
        "proposals": proposals,
        "section": section,
        "reviewed": reviewed,
    }

    return render(request_review, "symposion/reviews/review_list.html", ctx)


@login_required
def review_list(request_review_list, section_slug, user_pk):

    # if they're not a reviewer admin and they aren't the person whose
    # review list is being asked for, don't let them in
    if not request_review_list.user.has_perm("reviews.can_manage_%s" % section_slug):
        if not request_review_list.user.pk == user_pk:
            return render(request_review_list, "symposion/reviews/access_not_permitted.html", "you do not have access to review lists")

    queryset = ProposalBase.objects.select_related("speaker__user", "result")
    reviewed = LatestVote.objects.filter(user__pk=user_pk).values_list("proposal", flat=True)
    queryset = queryset.filter(pk__in=reviewed)
    proposals = queryset.order_by("submitted")

    admin = request_review_list.user.has_perm("reviews.can_manage_%s" % section_slug)

    proposals = proposals_generator(request_review_list, proposals, user_pk=user_pk, check_speaker=not admin)

    ctx = {
        "proposals": proposals,
    }
    return render(request_review_list, "symposion/reviews/review_list.html", ctx)


@login_required
def review_admin(request_review_admin, section_slug):

    if not request_review_admin.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_review_admin, "symposion/reviews/access_not_permitted.html", "you do not have access to administer reviews")

    def reviewers():
        already_seen = set()

        for team in Team.objects.filter(permissions__codename="can_review_%s" % section_slug):
            for membership in team.memberships.filter(Q(state="member") | Q(state="manager")):
                user = membership.user
                if user.pk in already_seen:
                    continue
                already_seen.add(user.pk)

                user.comment_count = Review.objects.filter(user=user).count()
                user.total_votes = LatestVote.objects.filter(user=user).count()
                user.plus_one = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.PLUS_ONE
                ).count()
                user.plus_zero = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.PLUS_ZERO
                ).count()
                user.minus_zero = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.MINUS_ZERO
                ).count()
                user.minus_one = LatestVote.objects.filter(
                    user=user,
                    vote=LatestVote.VOTES.MINUS_ONE
                ).count()

                yield user

    ctx = {
        "section_slug": section_slug,
        "reviewers": reviewers(),
    }
    return render(request_review_admin, "symposion/reviews/review_admin.html", ctx)

@login_required
def review_detail(request_review_detail, pk):

    proposals = ProposalBase.objects.select_related("result").select_subclasses()
    proposal = get_object_or_404(proposals, pk=pk)

    if not request_review_detail.user.has_perm("reviews.can_review_%s" % proposal.kind.section.slug):
        return render(request_review_detail, "symposion/reviews/access_not_permitted.html", "you do not have access to review details")

    speakers = [s.user for s in proposal.speakers()]

    if not request_review_detail.user.is_superuser and request_review_detail.user in speakers:
        return render(request_review_detail, "symposion/reviews/access_not_permitted.html", "you do not have access to review details for speakers")

    admin = request_review_detail.user.is_staff

    try:
        latest_vote = LatestVote.objects.get(proposal=proposal, user=request_review_detail.user)
    except LatestVote.DoesNotExist:
        latest_vote = None

    if request_review_detail.method == "POST":
        if request_review_detail.user in speakers:
            return render(request_review_detail, "symposion/reviews/access_not_permitted.html", "you do not have access to review details for speakers")

        if "vote_submit" in request_review_detail.POST:
            review_form = ReviewForm(request_review_detail.POST)
            if review_form.is_valid():

                review = review_form.save(commit=False)
                review.user = request_review_detail.user
                review.proposal = proposal
                review.save()

                return redirect(request_review_detail.path)
            else:
                message_form = SpeakerCommentForm()
        elif "message_submit" in request_review_detail.POST:
            message_form = SpeakerCommentForm(request_review_detail.POST)
            if message_form.is_valid():

                message = message_form.save(commit=False)
                message.user = request_review_detail.user
                message.proposal = proposal
                message.save()

                for speaker in speakers:
                    if speaker and speaker.email:
                        ctx = {
                            "proposal": proposal,
                            "message": message,
                            "reviewer": False,
                        }
                        send_email(
                            [speaker.email], "proposal_new_message",
                            context=ctx
                        )

                return redirect(request_review_detail.path)
            else:
                initial = {}
                if latest_vote:
                    initial["vote"] = latest_vote.vote
                if request_review_detail.user in speakers:
                    review_form = None
                else:
                    review_form = ReviewForm(initial=initial)
        elif "result_submit" in request_review_detail.POST:
            if admin:
                result = request_review_detail.POST["result_submit"]

                if result == "accept":
                    proposal.result.status = "accepted"
                    proposal.result.save()
                elif result == "reject":
                    proposal.result.status = "rejected"
                    proposal.result.save()
                elif result == "undecide":
                    proposal.result.status = "undecided"
                    proposal.result.save()
                elif result == "standby":
                    proposal.result.status = "standby"
                    proposal.result.save()

            return redirect(request_review_detail.path)
    else:
        initial = {}
        if latest_vote:
            initial["vote"] = latest_vote.vote
        if request_review_detail.user in speakers:
            review_form = None
        else:
            review_form = ReviewForm(initial=initial)
        message_form = SpeakerCommentForm()

    proposal.comment_count = proposal.result.comment_count
    proposal.total_votes = proposal.result.vote_count
    proposal.plus_one = proposal.result.plus_one
    proposal.plus_zero = proposal.result.plus_zero
    proposal.minus_zero = proposal.result.minus_zero
    proposal.minus_one = proposal.result.minus_one

    reviews = Review.objects.filter(proposal=proposal).order_by("-submitted_at")
    messages = proposal.messages.order_by("submitted_at")

    return render(request_review_detail, "symposion/reviews/review_detail.html", {
        "proposal": proposal,
        "latest_vote": latest_vote,
        "reviews": reviews,
        "review_messages": messages,
        "review_form": review_form,
        "message_form": message_form
    })


@login_required
@require_POST
def review_delete(request_delete, pk):
    review = get_object_or_404(Review, pk=pk)
    section_slug = review.section.slug

    if not request_delete.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_delete, "symposion/reviews/access_not_permitted.html", "you do not have access to delete users")

    review = get_object_or_404(Review, pk=pk)
    review.delete()

    return redirect("review_detail", pk=review.proposal.pk)


@login_required
def review_status(request_review_status, section_slug=None, key=None):

    if not request_review_status.user.has_perm("reviews.can_review_%s" % section_slug):
        return render(request_review_status, "symposion/reviews/access_not_permitted.html", "you do not have access to review status")

    VOTE_THRESHOLD = settings.SYMPOSION_VOTE_THRESHOLD

    ctx = {
        "section_slug": section_slug,
        "vote_threshold": VOTE_THRESHOLD,
    }

    queryset = ProposalBase.objects.select_related("speaker__user", "result").select_subclasses()
    if section_slug:
        queryset = queryset.filter(kind__section__slug=section_slug)

    proposals = {
        # proposals with at least VOTE_THRESHOLD reviews and at least one +1 and no -1s, sorted by
        # the 'score'
        "positive": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__plus_one__gt=0,
                                    result__minus_one=0).order_by("-result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and at least one -1 and no +1s, reverse
        # sorted by the 'score'
        "negative": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one__gt=0,
                                    result__plus_one=0).order_by("result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and neither a +1 or a -1, sorted by total
        # votes (lowest first)
        "indifferent": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one=0,
                                       result__plus_one=0).order_by("result__vote_count"),
        # proposals with at least VOTE_THRESHOLD reviews and both a +1 and -1, sorted by total
        # votes (highest first)
        "controversial": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD,
                                         result__plus_one__gt=0, result__minus_one__gt=0)
        .order_by("-result__vote_count"),
        # proposals with fewer than VOTE_THRESHOLD reviews
        "too_few": queryset.filter(result__vote_count__lt=VOTE_THRESHOLD)
        .order_by("result__vote_count"),
    }

    admin = request_review_status.user.has_perm("reviews.can_manage_%s" % section_slug)

    for status in proposals:
        if key and key != status:
            continue
        proposals[status] = list(proposals_generator(request_review_status, proposals[status], check_speaker=not admin))

    if key:
        ctx.update({
            "key": key,
            "proposals": proposals[key],
        })
    else:
        ctx["proposals"] = proposals

    return render(request_review_status, "symposion/reviews/review_stats.html", ctx)


@login_required
def review_assignments(request_review_assignments):
    if not request_review_assignments.user.groups.filter(name="reviewers").exists():
        return render(request_review_assignments, "symposion/reviews/access_not_permitted.html", "you do not have access to review assignments")
    assignments = ReviewAssignment.objects.filter(
        user=request_review_assignments.user,
        opted_out=False
    )
    return render(request_review_assignments, "symposion/reviews/review_assignment.html", {
        "assignments": assignments,
    })


@login_required
@require_POST
def review_assignment_opt_out(request_review_assignment_opt_out, pk):
    review_assignment = get_object_or_404(
        ReviewAssignment, pk=pk, user=request_review_assignment_opt_out.user)
    if not review_assignment.opted_out:
        review_assignment.opted_out = True
        review_assignment.save()
        ReviewAssignment.create_assignments(
            review_assignment.proposal, origin=ReviewAssignment.AUTO_ASSIGNED_LATER)
    return redirect("review_assignments")


@login_required
def review_bulk_accept(request_review_bulk_accept, section_slug):
    if not request_review_bulk_accept.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_review_bulk_accept, "symposion/reviews/access_not_permitted.html", "you do not have access to bulk accept reviews")
    if request_review_bulk_accept.method == "POST":
        form = BulkPresentationForm(request_review_bulk_accept.POST)
        if form.is_valid():
            talk_ids = form.cleaned_data["talk_ids"].split(",")
            talks = ProposalBase.objects.filter(id__in=talk_ids).select_related("result")
            for talk in talks:
                talk.result.status = "accepted"
                talk.result.save()
            return redirect("review_section", section_slug=section_slug)
    else:
        form = BulkPresentationForm()

    return render(request_review_bulk_accept, "symposion/reviews/review_bulk_accept.html", {
        "form": form,
    })


@login_required
def result_notification(request_result_notification, section_slug, status):
    if not request_result_notification.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_result_notification, "symposion/reviews/access_not_permitted.html", "you do not have access to request result notifications")

    proposals = ProposalBase.objects.filter(kind__section__slug=section_slug, result__status=status).select_related("speaker__user", "result").select_subclasses()
    notification_templates = NotificationTemplate.objects.all()

    ctx = {
        "section_slug": section_slug,
        "status": status,
        "proposals": proposals,
        "notification_templates": notification_templates,
    }
    return render(request_result_notification, "symposion/reviews/result_notification.html", ctx)


@login_required
def result_notification_prepare(request_result_notification_prepare, section_slug, status):
    if request_result_notification_prepare.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not request_result_notification_prepare.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_result_notification_prepare, "symposion/reviews/access_not_permitted.html", "you do not have access to manage reviews")

    proposal_pks = []
    try:
        for pk in request_result_notification_prepare.POST.getlist("_selected_action"):
            proposal_pks.append(int(pk))
    except ValueError:
        return HttpResponseBadRequest()
    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()

    notification_template_pk = request_result_notification_prepare.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None

    ctx = {
        "section_slug": section_slug,
        "status": status,
        "notification_template": notification_template,
        "proposals": proposals,
        "proposal_pks": ",".join([str(pk) for pk in proposal_pks]),
    }
    return render(request_result_notification_prepare, "symposion/reviews/result_notification_prepare.html", ctx)

def accept_staff_suggestion(staffId):
    return 

@login_required
def result_notification_send(request_result_notification_send, section_slug, status):
    if request_result_notification_send.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not request_result_notification_send.user.has_perm("reviews.can_manage_%s" % section_slug):
        return render(request_result_notification_send, "symposion/reviews/access_not_permitted.html", "you do not have access to request result notifications")

    if not all([k in request_result_notification_send.POST for k in ["proposal_pks", "from_address", "subject", "body"]]):
        return HttpResponseBadRequest()

    try:
        proposal_pks = [int(pk) for pk in request_result_notification_send.POST["proposal_pks"].split(",")]
    except ValueError:
        return HttpResponseBadRequest()

    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()

    notification_template_pk = request_result_notification_send.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None

    emails = []

    for proposal in proposals:
        rn = ResultNotification()
        rn.proposal = proposal
        rn.template = notification_template
        rn.to_address = proposal.speaker_email
        rn.from_address = request_result_notification_send.POST["from_address"]
        rn.subject = request_result_notification_send.POST["subject"]
        rn.body = Template(request_result_notification_send.POST["body"]).render(
            Context({
                "proposal": proposal.notification_email_context()
            })
        )
        rn.save()
        emails.append(rn.email_args)

    send_mass_mail(emails)

    return redirect("result_notification", section_slug=section_slug, status=status)



@login_required
def review_staff_comment(request_review_staff_comment, section_slug):
    if not request_review_staff_comment.user.has_perm("reviews.can_manage%s" % section_slug):
        return render(request_review_staff_comment,"symposion/reviews/access_not_permitted.html", "you do not have permission to accept staff reviews")
    if request_review_staff_comment.method == "POST":
        form = StaffCommentForm(request_review_staff_comment.POST)
        # TODO: complete implementation of staff comment form - split and mark accepted