from backend.models import *
from rest_framework import serializers


class AtentionQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtentionQueue
        fields = ('id', 'specialty', 'current_size', 'description')


class HealthCenterSerializer(serializers.ModelSerializer):
    queues = serializers.StringRelatedField(read_only=True, many=True)
    ranking = serializers.ReadOnlyField(source='get_ranking')

    class Meta:
        model = HealthCenter
        fields = ('id', 'name', 'address', 'position', 'queues','ranking')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class RecommendationDataSerializer(serializers.ModelSerializer):

    healthcenter = HealthCenterSerializer(read_only=True)

    class Meta:
        model = RecommendationData
        fields = '__all__'


class AtentionRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttentionRecord
        fields = '__all__'

