from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

]
