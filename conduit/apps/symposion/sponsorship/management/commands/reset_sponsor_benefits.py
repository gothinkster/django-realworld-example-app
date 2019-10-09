from django.core.management.base import BaseCommand

from symposion.sponsorship.models import Sponsor, SponsorBenefit, SponsorLevel


class Command(BaseCommand):

    def handle(self, *args, **options):
        for sponsor in Sponsor.objects.all():
            level = None
            try:
                level = sponsor.level
            except SponsorLevel.DoesNotExist:
                pass
            if level:
                for benefit_level in level.benefit_levels.all():
                    # Create all needed benefits if they don't exist already
                    sponsor_benefit, created = SponsorBenefit.objects.get_or_create(
                        sponsor=sponsor, benefit=benefit_level.benefit)

                    if created:
                        print "created", sponsor_benefit, "for", sponsor

                    # and set to default limits for this level.
                    sponsor_benefit.max_words = benefit_level.max_words
                    sponsor_benefit.other_limits = benefit_level.other_limits

                    # and set to active
                    sponsor_benefit.active = True

                    # @@@ We don't call sponsor_benefit.clean here. This means
                    # that if the sponsorship level for a sponsor is adjusted
                    # downwards, an existing too-long text entry can remain,
                    # and won't raise a validation error until it's next
                    # edited.
                    sponsor_benefit.save()
