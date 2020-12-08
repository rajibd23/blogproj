from django.conf.urls import url
from django.urls import path
from .views import ProfileHomeView, ProfileIdentite

urlpatterns = [
    path('/profile', ProfileHomeView.as_view(), name='profile-home'),
    path('identity/(?P<pk>[0-9]+)/',
        ProfileIdentite.as_view(), name='profile-identity-form'),
]