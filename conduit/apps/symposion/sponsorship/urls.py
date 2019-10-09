from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    sponsor_apply,
    sponsor_add,
    sponsor_zip_logo_files,
    sponsor_detail
)

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="symposion/sponsorship/list.html"), name="sponsor_list"),
    url(r"^apply/$", sponsor_apply, name="sponsor_apply"),
    url(r"^add/$", sponsor_add, name="sponsor_add"),
    url(r"^ziplogos/$", sponsor_zip_logo_files, name="sponsor_zip_logos"),
    url(r"^(?P<pk>\d+)/$", sponsor_detail, name="sponsor_detail"),
]
