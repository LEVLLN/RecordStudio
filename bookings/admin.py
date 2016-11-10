from django.contrib import admin

# Register your models here.
from django.contrib import admin
from bookings.models import Schedule, Booking, Record


@admin.register(Booking)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass
