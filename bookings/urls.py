from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^', views.home, name='home'),
    url(r'^book/', views.booking, name='booking'),
    url(r'^test/', views.test, name='test'),

]
