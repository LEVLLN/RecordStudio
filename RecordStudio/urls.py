from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('bookings.urls')),
    url(r'^accounts/', include('accounts.urls'), name='acc'),
    url(r'^admin/', admin.site.urls),

]
