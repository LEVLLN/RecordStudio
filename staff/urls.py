from django.conf.urls import url
from bookings import views as booking_views
from accounts import views as account_views
from staff import views

urlpatterns = [
    url(r'^$', views.StaffLoginPageView.as_view(), name='stuff_main_page'),
    url(r'^settings/', account_views.PasswordChangeView.as_view(), name='settings'),
    url(r'^profile/', views.StaffProfilePageView.as_view(), name='staff_profile'),
    url(r'^add/', views.SoundmanAddView.as_view(), name='soundman_add'),
    url(r'^booking/(?P<booking_id>[0-9]+)/cancel/', booking_views.cancel_booking, name="cancel_booking"),
]