from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.sites.models import Site


def send_email(to, kind, **kwargs):

    current_site = Site.objects.get_current()

    ctx = {
        "current_site": current_site,
        "STATIC_URL": settings.STATIC_URL,
    }
    ctx.update(kwargs.get("context", {}))
    subject = "[%s] %s" % (
        current_site.name,
        render_to_string("symposion/emails/%s/subject.txt" % kind, ctx).strip()
    )

    message_html = render_to_string("symposion/emails/%s/message.html" % kind, ctx)
    message_plaintext = strip_tags(message_html)

    from_email = settings.DEFAULT_FROM_EMAIL

    email = EmailMultiAlternatives(subject, message_plaintext, from_email, to)
    email.attach_alternative(message_html, "text/html")
    email.send()
