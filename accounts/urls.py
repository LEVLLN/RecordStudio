from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name="reg"),
    url(r'^administrator_page', views.administrators_page, name='adm'),
    url(r'^soundman', views.soundman_page, name='sndmn')
]
