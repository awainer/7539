from backend.models import *
from rest_framework import serializers


class AtentionQueueSerializer(serializers.ModelSerializer):
    wait_time = serializers.ReadOnlyField(source='get_average_wait_time')
    size = serializers.ReadOnlyField()
    health_center_name = serializers.ReadOnlyField(source='health_center.name')
    class Meta:
        model = AtentionQueue
        fields = ('id', 'specialty', 'description', 'health_center','health_center_name', 'wait_time', 'size', 'atention_count',
        'atention_time_total','max_capacity')


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

class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = '__all__'

class TriageScaleLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TriageScaleLevel
        fields = '__all__'


class UpcomingPatientFeedMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpcomingPatientFeedMessage
        fields = '__all__'