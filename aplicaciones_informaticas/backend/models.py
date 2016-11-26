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

    def setDefaultHealthCenter(self):
        self.name = "Hospital Central Bs As"
        self.address = "Corrientes 2856"
        self.phone = "497-4156"
        self.set_position(-34.604546, -58.40595)


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

delete_reason = (
    ('1','Fue atendido.'),
    ('2','Fue recategorizado de especialidad.'),
    ('3','Se retiró sin ser atendido.')
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
        return Patient.objects.filter(queue=self.id)

    def get_patient(self,patient_id):
        return Patient.objects.filter(queue=self.id).get(pk=patient_id)

    def get_average_wait_time(self):
        return self.current_size * float(self.average_attention_time) / self.attention_channels

class Patient(models.Model):
    triageScale = models.CharField(max_length=1, choices=triage_levels)
    waitTime = models.IntegerField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField
    queue = models.ForeignKey(AtentionQueue)
    def __str__(self):
        return str(self.id) + ' - Start:' + str(self.startTime)

class RecommendationData(models.Model):
    '''
          name:
        type: string
      address:
        type: string
      waitTime:
        description: Tiempo de espera estimado de atención (en minutos).
        type: string
      travelTime:
        description: Tiempo de viaje hasta llegar al hospital (en minutos).
        type: string
      patientsWaiting:
        description: Cantidad de gente en la cola esperando a ser atendida.
        type: integer
      distance:
        description: Distancia hacia el hospital (en metros).
        type: string
      ranking:
        description: Valor numérico de la popularidad del hospital, del 1 al 5.
        type: number
        format: double
    '''

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    waitTime = models.PositiveIntegerField(default=0)
    travelTime= models.PositiveIntegerField(default=0)
    patientsWaiting = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    ranking = models.FloatField()





class RecommendationEngine(models.Model):

    def get_random_recommendation():
        rec1 = RecommendationData(name="foo",address="bar", travelTime=10, patientsWaiting=5, distance=4, ranking=1.8)
        rec2 = RecommendationData(name="asdasd",address="fasdasdsad", travelTime=100, patientsWaiting=5, distance=4, ranking=2.8)
        return [rec1,rec2]


