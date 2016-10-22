from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create_booking',views.create_booking,name='create_booking')
]
