from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login', views.AuthenticationView.login, name='login'),
    url(r'^logout', views.AuthenticationView.logout, name='logout'),
    url(r'^register', views.RegistrationView.register, name="reg"),
    url(r'^my_profile', views.AuthenticationView.check_for_permission, name='profiles'),
    url(r'^forget', views.ForgetPasswordView.forget, name='forget'),
]
