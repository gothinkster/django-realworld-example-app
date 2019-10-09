from django import template

from conduit.apps.symposion.reviews.models import ReviewAssignment


register = template.Library()


@register.assignment_tag(takes_context=True)
def review_assignments(context):
    request = context["request"]
    assignments = ReviewAssignment.objects.filter(user=request.user)
    return assignments
