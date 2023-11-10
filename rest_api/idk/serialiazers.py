from rest_framework import serializers
from .models import Station, Train


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['id']


class TrainSerializer(serializers.ModelSerializer):
    departure_station = StationSerializer()
    arrival_station = StationSerializer()
    class Meta:
        model = Train
        fields = '__all__'
        