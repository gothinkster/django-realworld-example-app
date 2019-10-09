from django.db.models import Q

from .models import Team


class TeamPermissionsBackend(object):

    def authenticate(self, username=None, password=None):
        return None

    def get_team_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        team memberships.
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, "_team_perm_cache"):
            memberships = Team.objects.filter(
                Q(memberships__user=user_obj),
                Q(memberships__state="manager") | Q(memberships__state="member"),
            )
            perms = memberships.values_list(
                "permissions__content_type__app_label",
                "permissions__codename"
            ).order_by()
            user_obj._team_perm_cache = set(["%s.%s" % (ct, name) for ct, name in perms])
        return user_obj._team_perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_team_permissions(user_obj, obj)
