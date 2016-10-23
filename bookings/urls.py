from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^creating_booking', views.creating_booking, name='creating_booking'),
]
