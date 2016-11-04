from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='main_page'),
    url(r'^about', views.about, name='about'),
    url(r'^creating_booking', views.creating_booking, name='creating_booking'),
    url(r'creating/show_soundmans', views.show_soundmans, name='show_soundmans'),
    url(r'creating/show_soundman_schedule/(?P<soundman_id>[0-9]+)/$', views.show_soundman_schedule, name='show_soundman_schedule'),
]
