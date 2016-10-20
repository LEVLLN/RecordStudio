from django.contrib import admin

# Register your models here.
from django.contrib import admin
from bookings.models import Schedule, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
