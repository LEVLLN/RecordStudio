from django.conf.urls import url, include
from accounts import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name="reg"),
]
