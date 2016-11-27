from backend.models import *
from rest_framework import serializers


#class HealthCenterSerializer(serializers.HyperlinkedModelSerializer):



class AtentionQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtentionQueue
        fields = ('id','specialty','current_size','description')

class HealthCenterSerializer(serializers.ModelSerializer):
    #queues = serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    queues = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = HealthCenter
        fields = ('id','name','address','position','queues')

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class RecommendationDataSerializer(serializers.ModelSerializer):
    #healthcenter = serializers.PrimaryKeyRelatedField(read_only=True)
    healthcenter = HealthCenterSerializer(read_only=True)
    class Meta:
        model = RecommendationData
        fields = '__all__'