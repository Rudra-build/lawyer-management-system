from django.db import models
from lawyer.models import Lawyer

# Create your models here.
class TimeSlot(models.Model):
    lawyer= models.ForeignKey(Lawyer, on_delete=models.PROTECT)
    date= models.DateField()
    start_time = models.TimeField() #all time slots are 1 hr. ASSUMPTION
    booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)