# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.



class Schedule(models.Model):
    soundman = models.ForeignKey(User)
    start_of_the_day = models.TimeField()
    end_of_the_day = models.TimeField()
    DAY_OF_WEEK =(
        (1,"Monday"),
        (2,"Tuesday"),
        (3, "Wednesday"),
        (4,"Thursday"),
        (5, "Friday"),
        (6,"Saturday"),
        (7,"Sunday")

    )
    working_day = models.IntegerField(choices=DAY_OF_WEEK)


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations')
    soundman = models.ForeignKey(User, related_name='assigned_reservations')
    STATUS = (
        (1,'Active'),
        (2,'In progress'),
        (3,'Inactive')
    )
    is_active = models.IntegerField(choices=STATUS)
    start = models.DateTimeField()
    duration = models.DurationField()
