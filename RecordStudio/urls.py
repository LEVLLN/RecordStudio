from django.conf.urls import url, include
from django.contrib import admin

from accounts import views
from bookings import views as booking_views

urlpatterns = [
    url(r'^', include('bookings.urls'), name='bookings'),
    url(r'^accounts/', include('accounts.urls'), name='accounts'),
    url(r'^admin/', admin.site.urls),

    url(r'^staff/', views.StaffLoginPageView.as_view(), name='stuff_login_page'),
    url(r'^profile/', views.StaffProfilePageView.as_view(), name='staff_profile'),
    url(r'^booking/(?P<booking_id>[0-9]+)/cancel', booking_views.cancel_booking, name="cancel_booking"),


]
