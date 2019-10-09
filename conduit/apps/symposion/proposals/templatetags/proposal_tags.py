from django import template

from symposion.proposals.models import AdditionalSpeaker


register = template.Library()


class AssociatedProposalsNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        request = context["request"]
        if request.user.speaker_profile:
            pending = AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED
            speaker = request.user.speaker_profile
            queryset = AdditionalSpeaker.objects.filter(speaker=speaker, status=pending)
            context[self.context_var] = [item.proposalbase for item in queryset]
        else:
            context[self.context_var] = None
        return u""


class PendingProposalsNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        request = context["request"]
        if request.user.speaker_profile:
            pending = AdditionalSpeaker.SPEAKING_STATUS_PENDING
            speaker = request.user.speaker_profile
            queryset = AdditionalSpeaker.objects.filter(speaker=speaker, status=pending)
            context[self.context_var] = [item.proposalbase for item in queryset]
        else:
            context[self.context_var] = None
        return u""


@register.tag
def pending_proposals(parser, token):
    """
    {% pending_proposals as pending_proposals %}
    """
    return PendingProposalsNode.handle_token(parser, token)


@register.tag
def associated_proposals(parser, token):
    """
    {% associated_proposals as associated_proposals %}
    """
    return AssociatedProposalsNode.handle_token(parser, token)
