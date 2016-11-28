from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = [
    url(r'^login', views.AuthenticationView.as_view(), name='login'),
    url(r'^logout', views.AuthenticationView.logout, name='logout'),
    url(r'^my_profile', views.CustomerProfileView.as_view(), name='profiles'),
    url(r'^settings', login_required(views.PasswordChangeView.as_view()), name='settings'),

    url(r'^register', views.RegistrationView.as_view(), name="reg"),

    url(r'^forget', views.ForgetPasswordView.as_view(), name='forget'),
    url(r'^confirm', views.ConfirmView.as_view(), name='confirmation'),
    url(r'^resend', views.ConfirmView.resend_email, name='resend'),

    
]
