from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='main_page'),
    url(r'^about', views.about, name='about'),
    url(r'^creating_booking', views.creating_booking, name='creating_booking'),
    url(r'step_1', views.show_soundmans, name='step_1'),
    url(r'step_2/(?P<soundman_id>[0-9]+)/(?P<year>\d{4})$', views.show_schedule, name='step_2'),
]
