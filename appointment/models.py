from django.db import models
from client.models import Client
from case.models import Case
from timeslot.models import TimeSlot


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    timeslot = models.OneToOneField (TimeSlot , on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default= 'Scheduled') #other statuses can be scheduled, completed, cancelled, no-show
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)
