from django.conf.urls import url

from .views import ProfileFollowAPIView, ProfileRetrieveAPIView

urlpatterns = [
    url(r'^profiles/(?P<username>\w+)/?$', ProfileRetrieveAPIView.as_view()),
    url(r'^profiles/(?P<username>\w+)/follow/?$',
        ProfileFollowAPIView.as_view()),
]
