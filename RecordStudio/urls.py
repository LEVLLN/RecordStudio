from django.conf.urls import url, include
from django.contrib import admin

from accounts import views
from bookings import views as booking_views

urlpatterns = [
    url(r'^', include('bookings.urls'), name='booking'),
    url(r'^accounts/', include('accounts.urls'), name='acc'),
    url(r'^admin/', admin.site.urls),

    url(r'^staff/', views.StuffProfileLoginPageView.as_view(), name='stuffloginpage'),
    url(r'^booking/(?P<booking_id>[0-9]+)/cancel', booking_views.cancel_booking, name="cancel_booking"),

]
