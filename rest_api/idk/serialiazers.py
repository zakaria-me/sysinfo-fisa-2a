from rest_framework import serializers
from .models import SeatGroup, Station, Train

class SeatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatGroup
        exclude = ['id', 'type']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['id']


class TrainSerializer(serializers.ModelSerializer):
    departure_station = StationSerializer()
    arrival_station = StationSerializer()
    first_class_seats = SeatGroupSerializer()
    business_class_seats = SeatGroupSerializer()
    standard_class_seats = SeatGroupSerializer()
    class Meta:
        model = Train
        fields = '__all__'
        