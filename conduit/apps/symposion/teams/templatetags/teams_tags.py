from django import template

from symposion.teams.models import Team

register = template.Library()


class AvailableTeamsNode(template.Node):

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
        teams = []
        for team in Team.objects.all():
            state = team.get_state_for_user(request.user)
            if team.access == "open" and state is None:
                teams.append(team)
            elif request.user.is_staff and state is None:
                teams.append(team)
        context[self.context_var] = teams
        return u""


@register.tag
def available_teams(parser, token):
    """
    {% available_teams as available_teams %}
    """
    return AvailableTeamsNode.handle_token(parser, token)
