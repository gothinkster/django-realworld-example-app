from __future__ import unicode_literals

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from symposion.sponsorship.models import (
    Benefit,
    BENEFITS,
    BenefitLevel,
    Sponsor,
    SponsorBenefit,
    SponsorLevel,
)


class BenefitLevelInline(admin.TabularInline):
    model = BenefitLevel
    extra = 0


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0
    fieldsets = [
        (None, {
            "fields": [
                ("benefit", "active"),
                ("max_words", "other_limits"),
                "text",
                "upload",
            ]
        })
    ]


class SponsorAdmin(admin.ModelAdmin):

    save_on_top = True
    fieldsets = [
        (None, {
            "fields": [
                ("name", "applicant"),
                ("level", "active"),
                "external_url",
                "annotation",
                ("contact_name", "contact_email")
            ]
        }),
        ("Metadata", {
            "fields": ["added"],
            "classes": ["collapse"]
        })
    ]
    inlines = [SponsorBenefitInline]
    list_filter = ["level", "active"]
    list_display = ["name", "external_url", "level", "active", "contact", "applicant_field"]

    def contact(self, sponsor):
        return mark_safe('<a href="mailto:%s">%s</a>' % (escape(sponsor.contact_email), escape(sponsor.contact_name)))

    def applicant_field(self, sponsor):
        name = sponsor.applicant.get_full_name()
        email = sponsor.applicant.email
        return mark_safe('<a href="mailto:%s">%s</a>' % (escape(email), escape(name)))
    applicant_field.short_description = _(u"Applicant")

    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields["active"].widget.choices = [
            ("1", _("unreviewed")),
            ("2", _("approved")),
            ("3", _("rejected"))
        ]
        return form

    # Define accessor functions for our benefit fields and add them to
    # list_display, so we can sort on them and give them sensible names.
    # Add the fields to list_filters while we're at it.
    for benefit in BENEFITS:
        benefit_name = benefit['name']
        field_name = benefit['field_name']

        def func_generator(ben):
            def column_func(obj):
                return getattr(obj, ben['field_name'])
            column_func.short_description = ben['column_title']
            column_func.boolean = True
            column_func.admin_order_field = ben['field_name']
            return column_func
        list_display.append(func_generator(benefit))
        list_filter.append(field_name)

    def save_related(self, request, form, formsets, change):
        super(SponsorAdmin, self).save_related(request, form, formsets, change)
        obj = form.instance
        obj.save()


class BenefitAdmin(admin.ModelAdmin):

    list_display = ["name", "type", "description", "levels"]
    inlines = [BenefitLevelInline]

    def levels(self, benefit):
        return u", ".join(l.level.name for l in benefit.benefit_levels.all())


class SponsorLevelAdmin(admin.ModelAdmin):

    inlines = [BenefitLevelInline]


class SponsorBenefitAdmin(admin.ModelAdmin):
    list_display = ('benefit', 'sponsor', 'active', '_is_complete', 'show_text')

    def show_text(self, sponsor_benefit):
        if sponsor_benefit.text:
            return sponsor_benefit.text[:100]
        else:
            return _("None")


admin.site.register(SponsorLevel, SponsorLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(SponsorBenefit, SponsorBenefitAdmin)
