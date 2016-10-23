from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='main_page'),
    url(r'^creating_booking', views.creating_booking, name='creating_booking'),
]
