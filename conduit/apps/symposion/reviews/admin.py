from django.contrib import admin

from conduit.apps.symposion.reviews.models import NotificationTemplate, ProposalResult


admin.site.register(
    NotificationTemplate,
    list_display=[
        'label',
        'from_address',
        'subject'
    ]
)

admin.site.register(
    ProposalResult,
    list_display=['proposal', 'status', 'score', 'vote_count', 'accepted']
)
