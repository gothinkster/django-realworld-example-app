from __future__ import unicode_literals
try:
    from io import StringIO
except:
    # Python 2
    from cStringIO import StringIO
import itertools
import logging
import os
import time
from zipfile import ZipFile, ZipInfo

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from account.decorators import login_required

from symposion.sponsorship.forms import SponsorApplicationForm, \
    SponsorDetailsForm, SponsorBenefitsFormSet
from symposion.sponsorship.models import Benefit, Sponsor, SponsorBenefit, \
    SponsorLevel


log = logging.getLogger(__name__)


@login_required
def sponsor_apply(request):
    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save()
            if sponsor.sponsor_benefits.all():
                # Redirect user to sponsor_detail to give extra information.
                messages.success(request, _("Thank you for your sponsorship "
                                            "application. Please update your "
                                            "benefit details below."))
                return redirect("sponsor_detail", pk=sponsor.pk)
            else:
                messages.success(request, _("Thank you for your sponsorship "
                                            "application."))
                return redirect("dashboard")
    else:
        form = SponsorApplicationForm(user=request.user)

    return render_to_response("symposion/sponsorship/apply.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_add(request):
    if not request.user.is_staff:
        raise Http404()

    if request.method == "POST":
        form = SponsorApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            sponsor = form.save(commit=False)
            sponsor.active = True
            sponsor.save()
            return redirect("sponsor_detail", pk=sponsor.pk)
    else:
        form = SponsorApplicationForm(user=request.user)

    return render_to_response("symposion/sponsorship/add.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)

    if sponsor.applicant != request.user:
        return redirect("sponsor_list")

    formset_kwargs = {
        "instance": sponsor,
        "queryset": SponsorBenefit.objects.filter(active=True)
    }

    if request.method == "POST":

        form = SponsorDetailsForm(request.POST, instance=sponsor)
        formset = SponsorBenefitsFormSet(request.POST, request.FILES, **formset_kwargs)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            messages.success(request, _("Sponsorship details have been updated"))

            return redirect("dashboard")
    else:
        form = SponsorDetailsForm(instance=sponsor)
        formset = SponsorBenefitsFormSet(**formset_kwargs)

    return render_to_response("symposion/sponsorship/detail.html", {
        "sponsor": sponsor,
        "form": form,
        "formset": formset,
    }, context_instance=RequestContext(request))


@staff_member_required
def sponsor_export_data(request):
    sponsors = []
    data = ""

    for sponsor in Sponsor.objects.order_by("added"):
        d = {
            "name": sponsor.name,
            "url": sponsor.external_url,
            "level": (sponsor.level.order, sponsor.level.name),
            "description": "",
        }
        for sponsor_benefit in sponsor.sponsor_benefits.all():
            if sponsor_benefit.benefit_id == 2:
                d["description"] = sponsor_benefit.text
        sponsors.append(d)

    def izip_longest(*args):
        fv = None

        def sentinel(counter=([fv] * (len(args) - 1)).pop):
            yield counter()
        iters = [itertools.chain(it, sentinel(), itertools.repeat(fv)) for it in args]
        try:
            for tup in itertools.izip(*iters):
                yield tup
        except IndexError:
            pass

    def pairwise(iterable):
        a, b = itertools.tee(iterable)
        b.next()
        return izip_longest(a, b)

    def level_key(s):
        return s["level"]

    for level, level_sponsors in itertools.groupby(sorted(sponsors, key=level_key), level_key):
        data += "%s\n" % ("-" * (len(level[1]) + 4))
        data += "| %s |\n" % level[1]
        data += "%s\n\n" % ("-" * (len(level[1]) + 4))
        for sponsor, next in pairwise(level_sponsors):
            description = sponsor["description"].strip()
            description = description if description else "-- NO DESCRIPTION FOR THIS SPONSOR --"
            data += "%s\n\n%s" % (sponsor["name"], description)
            if next is not None:
                data += "\n\n%s\n\n" % ("-" * 80)
            else:
                data += "\n\n"

    return HttpResponse(data, content_type="text/plain;charset=utf-8")


@staff_member_required
def sponsor_zip_logo_files(request):
    """Return a zip file of sponsor web and print logos"""

    zip_stringio = StringIO()
    zipfile = ZipFile(zip_stringio, "w")
    try:
        benefits = Benefit.objects.all()
        for benefit in benefits:
            dir_name = benefit.name.lower().replace(" ", "_").replace('/', '_')
            for level in SponsorLevel.objects.all():
                level_name = level.name.lower().replace(" ", "_").replace('/', '_')
                for sponsor in Sponsor.objects.filter(level=level, active=True):
                    sponsor_name = sponsor.name.lower().replace(" ", "_").replace('/', '_')
                    full_dir = "/".join([dir_name, level_name, sponsor_name])
                    for sponsor_benefit in SponsorBenefit.objects.filter(
                        benefit=benefit,
                        sponsor=sponsor,
                        active=True,
                    ).exclude(upload=''):
                        if os.path.exists(sponsor_benefit.upload.path):
                            modtime = time.gmtime(os.stat(sponsor_benefit.upload.path).st_mtime)
                            with open(sponsor_benefit.upload.path, "rb") as f:
                                fname = os.path.split(sponsor_benefit.upload.name)[-1]
                                zipinfo = ZipInfo(filename=full_dir + "/" + fname,
                                                  date_time=modtime)
                                zipfile.writestr(zipinfo, f.read())
                        else:
                            log.debug("No such sponsor file: %s" % sponsor_benefit.upload.path)
    finally:
        zipfile.close()

    response = HttpResponse(zip_stringio.getvalue(),
                            content_type="application/zip")
    prefix = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]
    response['Content-Disposition'] = \
        'attachment; filename="%s_sponsorlogos.zip"' % prefix
    return response
