from django.conf.urls import url

from .views import ProfileRetrieveAPIView, ProfileFollowAPIView, ProfileFollow2APIView

urlpatterns = [
    url(r"^profiles/(?P<username>\w+)/?$", ProfileRetrieveAPIView.as_view()),
    url(r"^profiles/(?P<username>\w+)/follow/?$", ProfileFollowAPIView.as_view()),
    url(r"^profiles/(?P<username>\w+)/follow2/?$", ProfileFollow2APIView.as_view()),
]
