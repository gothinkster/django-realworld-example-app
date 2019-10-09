from __future__ import unicode_literals
import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader, Context

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.models import Site

from account.decorators import login_required

from symposion.schedule.forms import SlotEditForm, ScheduleSectionForm
from symposion.schedule.models import Schedule, Day, Slot, Presentation, Session, SessionRole
from symposion.schedule.timetable import TimeTable


def fetch_schedule(slug):
    qs = Schedule.objects.all()

    if slug is None:
        if qs.count() > 1:
            raise Http404()
        schedule = next(iter(qs), None)
        if schedule is None:
            raise Http404()
    else:
        schedule = get_object_or_404(qs, section__slug=slug)

    return schedule


def schedule_conference(request):

    if request.user.is_staff:
        schedules = Schedule.objects.filter(hidden=False)
    else:
        schedules = Schedule.objects.filter(published=True, hidden=False)

    sections = []
    for schedule in schedules:
        days_qs = Day.objects.filter(schedule=schedule)
        days = [TimeTable(day) for day in days_qs]
        sections.append({
            "schedule": schedule,
            "days": days,
        })

    ctx = {
        "sections": sections,
    }
    return render(request, "symposion/schedule/schedule_conference.html", ctx)


def schedule_detail(request, slug=None):

    schedule = fetch_schedule(slug)
    if not schedule.published and not request.user.is_staff:
        raise Http404()

    days_qs = Day.objects.filter(schedule=schedule)
    days = [TimeTable(day) for day in days_qs]

    ctx = {
        "schedule": schedule,
        "days": days,
    }
    return render(request, "symposion/schedule/schedule_detail.html", ctx)


def schedule_list(request, slug=None):
    schedule = fetch_schedule(slug)
    if not schedule.published and not request.user.is_staff:
        raise Http404()

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True)

    ctx = {
        "schedule": schedule,
        "presentations": presentations,
    }
    return render(request, "symposion/schedule/schedule_list.html", ctx)


def schedule_list_csv(request, slug=None):
    schedule = fetch_schedule(slug)
    if not schedule.published and not request.user.is_staff:
        raise Http404()

    presentations = Presentation.objects.filter(section=schedule.section)
    presentations = presentations.exclude(cancelled=True).order_by("id")
    response = HttpResponse(content_type="text/csv")

    if slug:
        file_slug = slug
    else:
        file_slug = "presentations"
    response["Content-Disposition"] = 'attachment; filename="%s.csv"' % file_slug

    response.write(loader.get_template("symposion/schedule/schedule_list.csv").render(Context({
        "presentations": presentations,

    })))
    return response


@login_required
def schedule_edit(request, slug=None):

    if not request.user.is_staff:
        raise Http404()

    schedule = fetch_schedule(slug)

    if request.method == "POST":
        form = ScheduleSectionForm(
            request.POST, request.FILES, schedule=schedule
        )
        if form.is_valid():
            if 'submit' in form.data:
                msg = form.build_schedule()
            elif 'delete' in form.data:
                msg = form.delete_schedule()
            messages.add_message(request, msg[0], msg[1])
    else:
        form = ScheduleSectionForm(schedule=schedule)
    days_qs = Day.objects.filter(schedule=schedule)
    days = [TimeTable(day) for day in days_qs]
    ctx = {
        "schedule": schedule,
        "days": days,
        "form": form
    }
    return render(request, "symposion/schedule/schedule_edit.html", ctx)


@login_required
def schedule_slot_edit(request, slug, slot_pk):

    if not request.user.is_staff:
        raise Http404()

    slot = get_object_or_404(Slot, day__schedule__section__slug=slug, pk=slot_pk)

    if request.method == "POST":
        form = SlotEditForm(request.POST, slot=slot)
        if form.is_valid():
            save = False
            if "content_override" in form.cleaned_data:
                slot.content_override = form.cleaned_data["content_override"]
                save = True
            if "presentation" in form.cleaned_data:
                presentation = form.cleaned_data["presentation"]
                if presentation is None:
                    slot.unassign()
                else:
                    slot.assign(presentation)
            if save:
                slot.save()
        return redirect("schedule_edit", slug)
    else:
        form = SlotEditForm(slot=slot)
        ctx = {
            "slug": slug,
            "form": form,
            "slot": slot,
        }
        return render(request, "symposion/schedule/_slot_edit.html", ctx)


def schedule_presentation_detail(request, pk):

    presentation = get_object_or_404(Presentation, pk=pk)
    if presentation.slot:
        schedule = presentation.slot.day.schedule
        if not schedule.published and not request.user.is_staff:
            raise Http404()
    else:
        schedule = None

    ctx = {
        "presentation": presentation,
        "schedule": schedule,
    }
    return render(request, "symposion/schedule/presentation_detail.html", ctx)


def schedule_json(request):
    slots = Slot.objects.filter(
        day__schedule__published=True,
        day__schedule__hidden=False
    ).order_by("start")

    protocol = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
    data = []
    for slot in slots:
        slot_data = {
            "room": ", ".join(room["name"] for room in slot.rooms.values()),
            "rooms": [room["name"] for room in slot.rooms.values()],
            "start": slot.start_datetime.isoformat(),
            "end": slot.end_datetime.isoformat(),
            "duration": slot.length_in_minutes,
            "kind": slot.kind.label,
            "section": slot.day.schedule.section.slug,
            "conf_key": slot.pk,
            # TODO: models should be changed.
            # these are model features from other conferences that have forked symposion
            # these have been used almost everywhere and are good candidates for
            # base proposals
            "license": "CC BY",
            "tags": "",
            "released": True,
            "contact": [],


        }
        if hasattr(slot.content, "proposal"):
            slot_data.update({
                "name": slot.content.title,
                "authors": [s.name for s in slot.content.speakers()],
                "contact": [
                    s.email for s in slot.content.speakers()
                ] if request.user.is_staff else ["redacted"],
                "abstract": slot.content.abstract.raw,
                "description": slot.content.description.raw,
                "conf_url": "%s://%s%s" % (
                    protocol,
                    Site.objects.get_current().domain,
                    reverse("schedule_presentation_detail", args=[slot.content.pk])
                ),
                "cancelled": slot.content.cancelled,
            })
        else:
            slot_data.update({
                "name": slot.content_override.raw if slot.content_override else "Slot",
            })
        data.append(slot_data)

    return HttpResponse(
        json.dumps({"schedule": data}),
        content_type="application/json"
    )


def session_list(request):
    sessions = Session.objects.all().order_by('pk')

    return render(request, "symposion/schedule/session_list.html", {
        "sessions": sessions,
    })


@login_required
def session_staff_email(request):

    if not request.user.is_staff:
        return redirect("schedule_session_list")

    data = "\n".join(user.email for user in User.objects.filter(sessionrole__isnull=False).distinct())

    return HttpResponse(data, content_type="text/plain;charset=UTF-8")


def session_detail(request, session_id):

    session = get_object_or_404(Session, id=session_id)

    chair = None
    chair_denied = False
    chairs = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR).exclude(status=False)
    if chairs:
        chair = chairs[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_CHAIR, status=False):
                chair_denied = True

    runner = None
    runner_denied = False
    runners = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER).exclude(status=False)
    if runners:
        runner = runners[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_RUNNER, status=False):
                runner_denied = True

    if request.method == "POST" and request.user.is_authenticated():
        if not hasattr(request.user, "profile") or not request.user.profile.is_complete:
            response = redirect("profile_edit")
            response["Location"] += "?next=%s" % request.path
            return response

        role = request.POST.get("role")
        if role == "chair":
            if chair is None and not chair_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user).save()
        elif role == "runner":
            if runner is None and not runner_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user).save()
        elif role == "un-chair":
            if chair == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user)
                if session_role:
                    session_role[0].delete()
        elif role == "un-runner":
            if runner == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user)
                if session_role:
                    session_role[0].delete()

        return redirect("schedule_session_detail", session_id)

    return render(request, "symposion/schedule/session_detail.html", {
        "session": session,
        "chair": chair,
        "chair_denied": chair_denied,
        "runner": runner,
        "runner_denied": runner_denied,
    })
