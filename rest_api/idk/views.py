from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets, permissions, status

from idk.models import Train
from idk.serialiazers import TrainSerializer

# Create your views here.

# Train Filtering REST WS : one Rest services that finds and updates available
#   trains based on departure and arrival stations, outbound and return dates and time, number of
#   tickets and the travel class (First, Business or Standard) (see the figure below).


class TrainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Train.objects.all().order_by('departure_date')
    serializer_class = TrainSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        """
        Properly filter the queryset based on the query parameters.
        """
        queryset = super().get_queryset()

        filters = [
            "departure_station", "arrival_station", "departure_date", "arrival_date",
            "seats_number", "first_class_seats", "business_class_seats", "standard_class_seats"]
        
        for f in filters:
            value = self.request.query_params.get(f)
            if value:
                queryset = queryset.filter(**{f: value})
                # queryset = queryset.filter(**{f + "__icontains": value})  # if we want to use contains instead of exact match
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"detail": "No available trains."}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)