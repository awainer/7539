from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
import datetime
# Create your views here.

from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import list_route,detail_route
from backend.serializers import *
from rest_framework import serializers
#from aplicaciones_informaticas.backend.serializers import *
from backend.models import *


class HealthCenterViewSet(viewsets.ModelViewSet):
    queryset = HealthCenter.objects.all()
    serializer_class = HealthCenterSerializer
    

    def retrieve(self, request, pk=None):
        queryset = HealthCenter.objects.all()
        hc = get_object_or_404(queryset, pk=pk)
        serializer = HealthCenterSerializer(hc)
        return Response(serializer.data)

#    @detail_route()
#    def queue(self, request, pk=None):
#        queryset = HealthCenter.objects.all()
#        return Response("SADASDSADAS")
#        #hc = get_object_or_404(queryset, pk=pk)


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

    #  curl -v  -XPOST --data "{\"triage_scale\":3 }" http://localhost:8000/api/v1/hospitals/38/queue/2/patients

    def add_patient(self,request,hc_id=None, queue_id=None):
        json_data = json.loads( request.body.decode('utf-8') )
        print(queue_id)
        queue =  AtentionQueue.objects.get(pk=int(queue_id))
        patient = Patient(triage_scale=json_data['triage_scale'],
                  waittime=60, # TODO hardcodeado
                  start_time=datetime.datetime.now(),
                  current_queue=queue
                    )
        patient.save()
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_patient(self, request,hc_id=None, queue_id=None, patient_id=None):
        raise Exception("not implemented")