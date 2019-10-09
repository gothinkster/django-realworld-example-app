from django.conf.urls import url

from .views import user_list

urlpatterns = [
    url(r"^users/$", user_list, name="user_list"),
]
