from django.db import models
from django.contrib.auth.models import User
from speciality.models import Speciality

# Create your models here.
class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username