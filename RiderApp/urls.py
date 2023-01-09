from django.conf.urls import include, re_path
from RiderApp import views


urlpatterns = [
    re_path(r'^ride$', views.RideAPI),
    re_path(r'^ride/(?P<ride_id>\d+)/$', views.RideAPI),
    re_path(r'^rider/(?P<rider_id>\d+)/$', views.RiderAPI)
]