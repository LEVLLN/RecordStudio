from django import template
from django.core.exceptions import ObjectDoesNotExist

from bookings.models import Record

register = template.Library()


@register.filter(name='money_back')
def money_back(values, booking_id):
    try:
        current_record = Record.objects.get(reservation_id=booking_id).money_back
        return str(current_record) + " рублей"
    except ObjectDoesNotExist:
        return "N/A"
