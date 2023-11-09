from rest_framework import serializers
from .models import Station, Train

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'
        

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'