from conduit.apps.core.renderers import ConduitJSONRenderer


class ProfileJSONRenderer(ConduitJSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'
