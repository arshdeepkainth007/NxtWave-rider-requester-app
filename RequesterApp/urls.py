from django.conf.urls import include, re_path
from RequesterApp import views


urlpatterns = [
    re_path(r'^request$', views.RequestAPI),
    re_path(r'^request/(?P<request_id>\d+)/$', views.RequestAPI),
    re_path(r'^requester/$', views.RequesterAPI),
    re_path(r'^request/match/(?P<request_id>\d+)/$', views.MatchingRidesAPI),
    re_path(r'^request/apply$', views.MatchingRidesAPI)
]