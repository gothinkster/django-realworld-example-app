from django.core.management.base import BaseCommand

from conduit.apps.symposion.reviews.models import ReviewAssignment
from conduit.apps.symposion.proposals.models import ProposalBase


class Command(BaseCommand):

    def handle(self, *args, **options):
        for proposal in ProposalBase.objects.filter(cancelled=0):
            print "Creating assignments for %s" % (proposal.title,)
            ReviewAssignment.create_assignments(proposal)
