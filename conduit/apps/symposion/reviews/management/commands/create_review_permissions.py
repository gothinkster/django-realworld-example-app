from django.core.management.base import BaseCommand

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from symposion.proposals.models import ProposalSection


class Command(BaseCommand):

    def handle(self, *args, **options):
        ct, created = ContentType.objects.get_or_create(
            model="",
            app_label="reviews",
            defaults={"name": "reviews"}
        )

        for ps in ProposalSection.objects.all():
            for action in ["review", "manage"]:
                perm, created = Permission.objects.get_or_create(
                    codename="can_%s_%s" % (action, ps.section.slug),
                    content_type__pk=ct.id,
                    defaults={"name": "Can %s %s" % (action, ps), "content_type": ct}
                )
                print perm
