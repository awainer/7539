from backend.models import *
from rest_framework import serializers


class AtentionQueueSerializer(serializers.ModelSerializer):
    wait_time = serializers.ReadOnlyField(source='get_average_wait_time')
    size = serializers.ReadOnlyField()

    class Meta:
        model = AtentionQueue
        fields = ('id', 'specialty', 'description', 'health_center', 'wait_time', 'size', 'atention_count',
        'atention_time_total')


class HealthCenterSerializer(serializers.ModelSerializer):
    queues = serializers.StringRelatedField(read_only=True, many=True)
    ranking = serializers.ReadOnlyField(source='get_ranking')

    class Meta:
        model = HealthCenter
        fields = ('id', 'name', 'address', 'position', 'queues', 'ranking')


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

