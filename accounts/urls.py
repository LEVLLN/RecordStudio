from django.conf.urls import url
from accounts import views
from bookings import views as booking_views

urlpatterns = [
    url(r'^login', views.AuthenticationView.as_view(), name='login'),
    url(r'^logout', views.AuthenticationView.logout, name='logout'),
    url(r'^my_profile', views.AuthenticationView.check_for_permission, name='profiles'),
    url(r'^settings', views.PasswordChangeView.as_view(), name='settings'),

    url(r'^register', views.RegistrationView.as_view(), name="reg"),

    url(r'^forget', views.ForgetPasswordView.as_view(), name='forget'),
    url(r'^confirm', views.ConfirmView.as_view(), name='confirmation'),

    
]
