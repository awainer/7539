from django.db import models
from geoposition.fields import GeopositionField
from decimal import Decimal
from backend import geo_distance
import math

# Create your models here.


class HealthCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    position = GeopositionField()
    ratings = models.IntegerField()
    score = models.IntegerField()

    def set_position(self, x, y):
        self.position = GeopositionField(Decimal(x), Decimal(y))

    def get_ranking(self):
        if self.ratings == 0:
            return -1
        print (self.id,self.ratings, self.score)
        result = float(self.score) / self.ratings
        print(result)
        return result

    def rate(self, rate):
        self.score += rate
        self.ratings += 1
        self.save()

    def __str__(self):
        return self.name

    def get_wait_time_average(self):
        sum = 0
        for queue in AtentionQueue.objects.filter(health_center=self):
            sum += queue.get_average_wait_time()
        avg = round(sum / len(AtentionQueue.objects.filter(health_center=self)) / 60)
        return   avg

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
    atention_time_total = models.IntegerField(default=0)
    atention_count = models.IntegerField(default=0)
    attention_channels = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=255, default='')
    max_capacity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return  '%s - %s - %s' % (self.description,
                                  self.specialty.name,
                                  self.health_center.name)

    def get_all_patients(self):
        return Patient.objects.filter(queue=self.id)

    def size(self, max_triage_scale=None):
        if not max_triage_scale:
            return len(Patient.objects.filter(queue=self.id))
        else:
            return len([x for x in self.patients.filter()
                        if x.triageScale.max_wait_in_minutes <= max_triage_scale.max_wait_in_minutes])

    def get_patient(self, patient_id):
        return Patient.objects.filter(queue=self.id).get(pk=patient_id)

    def _get_average_wait_time(self):
        if self.atention_count == 0:
            return 600
        return float(self.atention_time_total) / self.atention_count

    def update_atention_time(self, time_in_seconds):
        self.atention_time_total += time_in_seconds
        self.atention_count += 1
        self.save()

    def get_average_wait_time(self, triage_scale=None):
        if not triage_scale:
            patients_before = len(self.patients.all())
        else:
            patients_before = 0
            for patient in self.patients.all():
                if patient.triageScale.max_wait_in_minutes <= triage_scale.max_wait_in_minutes:
                    patients_before += 1

        return patients_before * self._get_average_wait_time() / self.attention_channels


class Patient(models.Model):
    triageScale = models.ForeignKey(TriageScaleLevel)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField
    queue = models.ForeignKey(AtentionQueue, related_name='patients', null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.id, self.queue, self.startTime)

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
    queue_id = models.IntegerField(default=0)
    hc_id = models.IntegerField(default=0)


class RecommendationEngine(models.Model):
    gd = geo_distance.GeoDistance()

    def get_recommendation(latitude, longitude, specialty=None, triage_scale=None):

        result = []
        if not triage_scale:
            triage_scale = TriageScaleLevel.objects.get(pk=5)
        if not specialty:
            specialty = Specialty.objects.get(id=1)
        for queue in AtentionQueue.objects.filter(specialty=specialty):
            recdata = RecommendationEngine.build_recdata(queue, latitude, longitude, triage_scale)
            result.append(recdata)
        result.sort(key=lambda x: x.waitTime + x.travelTime)
        return result

    def get_all_recommendations(latitude, longitude):
        result = []

        for queue in AtentionQueue.objects.all():
            recdata = RecommendationEngine.build_recdata(queue, latitude, longitude)
            result.append(recdata)
        return result

    def build_recdata(queue, latitude, longitude, triage_scale):
        healthcenter = queue.health_center
        travel_time, travel_distance = RecommendationEngine.gd.get_travel_time_and_distance(
            (latitude, longitude), (float(healthcenter.position.latitude),
             float(healthcenter.position.longitude)))

        recdata = RecommendationData(id=queue.id,
                                     name=healthcenter.name.title(),
                                     address=healthcenter.address.title(),
                                     waitTime=queue.get_average_wait_time(triage_scale=triage_scale),
                                     travelTime=travel_time,
                                     patientsWaiting=queue.size(max_triage_scale=triage_scale),
                                     distance=travel_distance,
                                     ranking=healthcenter.get_ranking(),
                                     queue_id=queue.id,
                                     hc_id=healthcenter.id)
        return recdata

    def get_random_recommendation():
        rec1 = RecommendationData(name="foo", address="bar",
         travelTime=10, patientsWaiting=5, distance=4, ranking=1.8)
        rec2 = RecommendationData(name="asdasd", address="fasdasdsad",
        travelTime=100, patientsWaiting=5, distance=4, ranking=2.8)
        return [rec1, rec2]


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
    triageScale = models.ForeignKey(TriageScaleLevel)

    class Meta():
        verbose_name_plural = "Atention records"

    def __str__(self):
        return '%s - %s %s %s' % (self.health_center, self.queue, self.reason, self.waitTime)


class UpcomingPatientFeedMessage(models.Model):
    health_center = models.ForeignKey(HealthCenter, on_delete=models.CASCADE)
    queue = models.ForeignKey(AtentionQueue, on_delete=models.CASCADE)
    triageScale = models.ForeignKey(TriageScaleLevel)
    eta = models.DateTimeField()
    message_delivered = models.BooleanField(default=False)


class Reports(models.Model):

    def attention_per_hour(hc_id, date_from, date_to):

        days_in_report = (date_to - date_from).days
        if days_in_report == 0:
            days_in_report = 1

        qs = AttentionRecord.objects.filter(health_center=hc_id, startTime__range=[date_from, date_to])
        response_data = {}
        response_data['data'] = []

        specialties = set()

        for record in qs:
            specialties.add(record.queue.specialty.id)

        for specialty in specialties:
            capacity = 0
            for queue in AtentionQueue.objects.filter(health_center=hc_id, specialty=specialty):
                capacity += queue.max_capacity
            patients_per_hour = {x: 0 for x in range(24)}
            for record in qs:
                queue = record.queue
                if queue.specialty.id == specialty:
                    patients_per_hour[record.startTime.hour] += 1
            for hour in patients_per_hour:
                patients_per_hour[hour] = math.ceil(patients_per_hour[hour] / days_in_report)
            response_data['data'].append({'specialty': specialty,
                                          'capacity': capacity,
                                          'patients_per_hour': patients_per_hour})
        return response_data

    def attention_per_hour_all_healthcenters(date_from, date_to):
        response_data = {'data': []}
        for hc in HealthCenter.objects.all():
            response_data['data'].append({
                                  "healthcenter": hc.name,
                                  "data": Reports.attention_per_hour(hc.id, date_from, date_to)['data']
                                })
        return response_data

    def get_upcoming_patients_feed(id_hospital, mark_as_read=True):
        result = UpcomingPatientFeedMessage.objects.filter(health_center=id_hospital, message_delivered=False)
        if mark_as_read:
            for message in result:
                message.message_delivered = True
                message.save()

        return result