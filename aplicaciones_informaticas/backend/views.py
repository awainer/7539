import math
import json
import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from backend.serializers import *
from backend.models import *
from django.utils import timezone
import dateutil.parser
from django.http import HttpResponse

class HealthCenterViewSet(viewsets.ModelViewSet):
    queryset = HealthCenter.objects.all()
    serializer_class = HealthCenterSerializer

    def retrieve(self, request, pk=None):
        queryset = HealthCenter.objects.all()
        hc = get_object_or_404(queryset, pk=pk)
        serializer = HealthCenterSerializer(hc)
        return Response(serializer.data)

    def rate(self, request, hc_id=None):
        json_data = json.loads(request.body.decode('utf-8'))
        hc = HealthCenter.objects.get(pk=hc_id)
        hc.rate(json_data['rating'])
        return Response({"success": True})

    def get_average_wait(self, request):
        result = []
        for hc in HealthCenter.objects.all():
            avg = hc.get_wait_time_average()
            ranking = round(hc.get_ranking())
            if ranking == -1:
                ranking = "Sin calificaciones"
            html = "<p><strong>%s</strong></p>" % hc.name.title()
            html += "<p>Tiempo promedio de espera: %s minutos.</p>" % avg
            html += "<p>Ranking: %s<p>" % ranking
            data = {"id": hc.id, "html": html, "waitTime": avg}
            result.append(data)

        return HttpResponse(json.dumps(result), content_type="application/json")


class AtentionQueueViewSet(viewsets.ModelViewSet):
    queryset = AtentionQueue.objects.all()
    serializer_class = AtentionQueueSerializer

    def get_one_for_hc(self, request, hc_id=None, queue_id=None):
        queryset = AtentionQueue.objects.all().filter(health_center=hc_id)
        data = get_object_or_404(queryset, pk=queue_id)
        serializer = AtentionQueueSerializer(data)
        return Response(serializer.data)

    def get_all_for_hc(self, request, hc_id=None):
        queryset = AtentionQueue.objects.all().filter(health_center=hc_id)
        serializer = AtentionQueueSerializer(queryset, many=True)
        return Response(serializer.data)

    #  curl -v  -XPOST --data "{\"triageScale\":3 }" http://localhost:8000/api/v1/hospitals/38/queue/2/patients
    def add_patient(self, request, hc_id=None, queue_id=None):
        json_data = json.loads(request.body.decode('utf-8'))
        print(queue_id)
        queue = AtentionQueue.objects.get(pk=int(queue_id))
        triage_level = TriageScaleLevel.objects.get(pk=json_data['triageScale'])
        patient = Patient(triageScale=triage_level,
                  startTime=datetime.datetime.now(),
                  queue=queue)
        patient.save()
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_all_patients(self, request, hc_id=None, queue_id=None):
        queue = AtentionQueue.objects.get(pk=int(queue_id))
        patients = queue.get_all_patients()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def get_patient(self, request, hc_id=None, queue_id=None, patient_id=None):
        queue = AtentionQueue.objects.get(pk=int(queue_id))
        try:
            patient = queue.get_patient(patient_id)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status.HTTP_201_CREATED)
        except:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def delete_patient(self, request, hc_id=None, queue_id=None, patient_id=None):

        json_data = json.loads(request.body.decode('utf-8'))

        try:
            queue = AtentionQueue.objects.get(pk=int(queue_id))
            patient = queue.get_patient(patient_id)
            health_center = HealthCenter.objects.get(pk=hc_id)
            delete_reason = DeleteReason.objects.get(pk=json_data['reason'])
            startTime = patient.startTime
            endTime = timezone.now()
            waitTime = (endTime - startTime).seconds
            atention_record = AttentionRecord(health_center=health_center,
                                              queue=queue,
                                              patient=patient,
                                              reason=delete_reason,
                                              startTime=startTime,
                                              endTime=endTime,
                                              waitTime=waitTime,
                                              triageScale=patient.triageScale)
            if delete_reason.id != 3:
                queue.update_atention_time(waitTime)
            atention_record.save()
            patient.remove_from_queue()
            serializer = AtentionRecordSerializer(atention_record)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"success": False, "reason": str(e)}, status.HTTP_404_NOT_FOUND)


# curl  -v -XPOST  -d {}  http://localhost:8000/api/v1/hospitals/recommendation
class RecommendationEngineViewSet(viewsets.ModelViewSet):
    def get_recommendation(self, request):
        json_data = json.loads(request.body.decode('utf-8'))
        lat = json_data['latitude']
        lon = json_data['longitude']
        specialty = None
        triageScale = None

        if 'specialty' in json_data:
            specialty = Specialty.objects.get(pk=json_data['specialty'])
        if 'triageScale' in json_data:
            triageScale = TriageScaleLevel.objects.get(pk=json_data['triageScale'])

        print(json_data)
        recommendation_list = []
        for recommendation in RecommendationEngine.get_recommendation(lat, lon, specialty, triageScale):
            recommendation_serializer = RecommendationDataSerializer(recommendation)
            recommendation_list.append(recommendation_serializer.data)
        return Response(recommendation_list)

    def select_recommendation(self, request, hc_id=None, queue_id=None):
        json_data = json.loads(request.body.decode('utf-8'))
        triageScale = TriageScaleLevel.objects.get(pk=json_data['triageScale'])
        eta = dateutil.parser.parse(json_data['eta'])
        notification = UpcomingPatientFeedMessage(health_center=HealthCenter.objects.get(pk=hc_id),
                                                  queue=AtentionQueue.objects.get(pk=queue_id),
                                                  triageScale=triageScale,
                                                  eta=eta)
        notification.save()
        response_data = json.dumps({"status": "Success."})
        return HttpResponse(response_data, content_type="application/json")


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class TriageScaleLevelViewSet(viewsets.ModelViewSet):
    queryset = TriageScaleLevel.objects.all()
    serializer_class = TriageScaleLevelSerializer


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()

    def get_attention_per_hour(self, request):
        parsed_date_from = dateutil.parser.parse(request.GET.get('date_from'))
        parsed_date_to = dateutil.parser.parse(request.GET.get('date_to'))
        if 'hc_id' in request.GET:
            result = Reports.attention_per_hour(request.GET.get('hc_id'), parsed_date_from, parsed_date_to)
            return HttpResponse(json.dumps(result), content_type="application/json")

        result = Reports.attention_per_hour_all_healthcenters(parsed_date_from, parsed_date_to)
        return HttpResponse(json.dumps(result), content_type="application/json")

    def get_feed(self, request, hc_id=None):
        result = []
        for message in Reports.get_upcoming_patients_feed(hc_id):
            message_serializer = UpcomingPatientFeedMessageSerializer(message)
            result.append(message_serializer.data)
        return Response(result)
