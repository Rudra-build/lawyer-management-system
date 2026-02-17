from django.db import models
from client.models import Client
from speciality.models import Speciality
# Create your models here.

class Case(models.Model):
    title = models.CharField(max_length=150)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Open')
    case_notes = models.TextField(blank = True)

    def __str__(self):
        return self.title