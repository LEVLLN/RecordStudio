from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name="reg"),
    url(r'^my_profile', views.check_for_permission, name='profiles'),
]
