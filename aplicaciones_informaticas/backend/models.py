from __future__ import unicode_literals
import json
from django.db import models
from geoposition.fields import GeopositionField
from decimal import Decimal
from backend import geo_distance


# Create your models here.

class HealthCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    position = GeopositionField()
    ranking = models.IntegerField()

    def set_position(self, x, y):
        self.position = GeopositionField(Decimal(x), Decimal(y))

    def __str__(self):
        return self.name

    def setDefaultHealthCenter(self):
        self.name = "Hospital Central Bs As"
        self.address = "Corrientes 2856"
        self.phone = "497-4156"
        self.set_position(-34.604546, -58.40595)


class Specialty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = "Specialties"


class TriageScaleLevel(models.Model):
    description = models.CharField(max_length=40)
    max_wait_in_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s - %s minutos de espera" % (self.id, self.max_wait_in_minutes)


class AtentionQueue(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE,
                    related_name='queues')
    specialty = models.ForeignKey(Specialty)
    average_attention_time = models.PositiveIntegerField(default=600)
    attention_channels = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.description

    def get_all_patients(self):
        return Patient.objects.filter(queue=self.id)

    def size(self):
        return len(Patient.objects.filter(queue=self.id))

    def get_patient(self, patient_id):
        return Patient.objects.filter(queue=self.id).get(pk=patient_id)

    def get_average_wait_time(self, triage_scale=None):
        if not triage_scale:
            patients_before = len(self.patients.all())
        else:
            patients_before = 0
            for patient in self.patients.all():
                if patient.triaceScale.max_wait_in_minutes <= triage_scale.max_wait_in_minutes:
                    patients_before += 1

        return self.patients_before * float(self.average_attention_time) / self.attention_channels


class Patient(models.Model):
    triageScale = models.ForeignKey(TriageScaleLevel)
    waitTime = models.IntegerField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField
    queue = models.ForeignKey(AtentionQueue, related_name='patients')

    def __str__(self):
        return str(self.id) + ' - Start:' + str(self.startTime)

    def remove_from_queue(self):
        self.queue = None
        self.save()


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
    travelTime = models.PositiveIntegerField(default=0)
    patientsWaiting = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)
    ranking = models.FloatField()


class RecommendationEngine(models.Model):

    def get_all_recommendations(latitude, longitude):
        result = []
        gd = geo_distance.GeoDistance()
        for queue in AtentionQueue.objects.all():
            healthcenter = queue.health_center
            travel_time, travel_distance = gd.get_travel_time_and_distance((latitude,longitude),
                                                                           (float(healthcenter.position.latitude), float(healthcenter.position.longitude)) )

            recdata = RecommendationData(name = healthcenter.name,
                                         address = healthcenter.address,
                                         waitTime = queue.get_average_wait_time(),
                                         travelTime = travel_time,
                                         patientsWaiting = queue.size(),
                                         distance= travel_distance,
                                         ranking = healthcenter.ranking )
            result.append(recdata)
        return result

    def get_random_recommendation():
        rec1 = RecommendationData(name="foo",address="bar",
         travelTime=10, patientsWaiting=5, distance=4, ranking=1.8)
        rec2 = RecommendationData(name="asdasd",address="fasdasdsad",
        travelTime=100, patientsWaiting=5, distance=4, ranking=2.8)
        return [rec1,rec2]


class DeleteReason(models.Model):
    description = models.CharField(max_length=80)
    def __str__(self):
        return '%s - %s' % (self.id, self.description)

class AttentionRecord(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    queue = models.ForeignKey(AtentionQueue, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    reason = models.ForeignKey(DeleteReason)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    waitTime = models.PositiveIntegerField(default=0)
    triaceScale = models.ForeignKey(TriageScaleLevel)

    class Meta():
        verbose_name_plural = "Atention records"