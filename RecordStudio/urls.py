from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('bookings.urls'), name='bookings'),
    url(r'^accounts/', include('accounts.urls'), name='accounts'),
    url(r'^admin/', admin.site.urls),
    url(r'^staff/', include('staff.urls'), name='stuff_login_page'),
]
