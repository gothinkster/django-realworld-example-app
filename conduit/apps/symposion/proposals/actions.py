from __future__ import unicode_literals
import csv

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _


def export_as_csv_action(description=None, fields=None, exclude=None,
                         header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in Django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        if fields:
            fieldset = set(fields)
            field_names = fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=%s.csv" % unicode(opts).replace(".", "_")
        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow(
                [unicode(getattr(obj, field)).encode("utf-8", "replace") for field in field_names])
        return response
    if description is None:
        description = _("Export selected objects as CSV file")
    export_as_csv.short_description = description
    return export_as_csv
