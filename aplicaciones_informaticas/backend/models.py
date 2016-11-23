from __future__ import unicode_literals

from django.db import models
from geoposition.fields import GeopositionField
from decimal import Decimal
from collections import  deque

# Create your models here.
class HealthCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    position = GeopositionField()

    def set_position(self,x,y):
        position = GeopositionField(Decimal(x), Decimal(y))

    def __str__(self):
        return self.name



#class Specialty(models.Model):
#    name = models.CharField(max_length=255)
#    def __str__(self):
#        return self.name
#    class Meta():
#        verbose_name_plural = "Specialties"


triage_levels = (
      ('1', 'Atención inmediata (0 minutos de espera).'),
      ('2', 'Atención muy urgente (10 minutos de espera).'),
      ('3', 'Atención urgente (60 minutos de espera).'),
      ('4', 'Atención normal (120 minutos de espera).'),
      ('5', 'Atención no urgente (240 minutos de espera).')
      )

specialties = (
        ('1', 'Clínica'),
        ('2', 'Pediatría'),
        ('3', 'Odontología'),
        ('4', 'Cirujía'),
        ('5', 'Traumatología'),
        ('6', 'Oftalmología')
        )

class AtentionQueue(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE, related_name='queues')
    specialty  =  models.CharField(max_length=1, choices=specialties)
    current_size = models.PositiveIntegerField(default=0)
    average_attention_time = models.PositiveIntegerField(default=600)
    attention_channels = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=255, default='')
    priority_queues =  {}

    for priority in triage_levels:
        priority_queues[priority[0]] = deque()

    def __str__(self):
        return str(self.health_center) + ' - ' + str(self.specialty) + ' - ' + str(self.description)

    def get_all_patients(self):
        return AtentionQueue.patient_set()

    def get_average_wait_time(self):
        return self.current_size * float(self.average_attention_time) / self.attention_channels

class Patient(models.Model):
    triage_scale = models.CharField(max_length=1, choices=triage_levels)
    waittime = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField
    current_queue = models.ForeignKey(AtentionQueue, related_name='queue')
    def __str__(self):
        return str(self.id) + ' - Start:' + str(self.start_time)