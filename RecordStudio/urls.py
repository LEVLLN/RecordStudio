from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^accounts/', include('accounts.urls'), name='acc'),
    url(r'^admin/', admin.site.urls),
    url(r'^bookings/', include('bookings.urls'))

]
