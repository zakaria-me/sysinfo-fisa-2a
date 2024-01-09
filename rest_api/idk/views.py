from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status

from idk.models import Station, Train
from idk.serialiazers import StationSerializer, TrainSerializer

# Create your views here.

# Train Filtering REST WS : one Rest services that finds and updates available
#   trains based on departure and arrival stations, outbound and return dates and time, number of
#   tickets and the travel class (First, Business or Standard) (see the figure below).

class UnrestrictedPermission(permissions.BasePermission):
    """
    Allow unrestricted access.
    """
    def has_permission(self, request, view):
        return True  # Allow any request

class StationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Station.objects.all().order_by('name')
    serializer_class = StationSerializer
    permission_classes = [UnrestrictedPermission]

    def get_queryset(self):
        """
        Properly filter the queryset based on the query parameters.
        """
        queryset = super().get_queryset()

        filters = ["name", "city"]
        
        for f in filters:
            value = self.request.query_params.get(f)
            if value:
                queryset = queryset.filter(**{f + "__icontains": value})  # if we want to use contains instead of exact match
        return queryset
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  # Use pagination for the queryset

        if not page:
            return Response({"detail": "No corresponding stations."}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TrainViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Train.objects.all().order_by('departure_date')
    serializer_class = TrainSerializer
    permission_classes = [UnrestrictedPermission]


    def get_queryset(self):
        """
        Properly filter the queryset based on the query parameters.
        """
        queryset = super().get_queryset()

        filters = [
            "departure_date", "arrival_date", "seats_number", "first_class_seats",
            "business_class_seats", "standard_class_seats"]
        
        for f in filters:
            value = self.request.query_params.get(f)
            if value:
                queryset = queryset.filter(**{f: value})
                # queryset = queryset.filter(**{f + "__icontains": value})  # if we want to use contains instead of exact match
        stations = ["departure_station", "arrival_station"]
        for s in stations:
            value = self.request.query_params.get(s)
            if value:
                queryset = queryset.filter(**{s + "__name__icontains": value})

        return queryset
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if not queryset.exists():
            return Response({"detail": "No available trains."}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def seats_reservation(self, request, pk=None):
        """
        Reserve a seat in a train.
        """
        train = self.get_object()

        if train.is_full:
            return Response({"detail": "No available seats."}, status=status.HTTP_204_NO_CONTENT)
        
        seat_type = request.data.get('seat_type')
        reservation_quantity = int(request.data.get('quantity'))
        ticket_type = request.data.get('ticket_type')

        if not seat_type:
            return Response({"detail": "Please specify the seat type."}, status=status.HTTP_400_BAD_REQUEST)
        if seat_type not in ['first', 'business', 'standard']:
            return Response({"detail": "Invalid seat type."}, status=status.HTTP_400_BAD_REQUEST)
        if not reservation_quantity:
            return Response({"detail": "Please specify the number of seats."}, status=status.HTTP_400_BAD_REQUEST)
        if not ticket_type:
            return Response({"detail": "Please specify the ticket type."}, status=status.HTTP_400_BAD_REQUEST)
        if ticket_type not in ['flexible', 'fixed']:
            return Response({"detail": "Invalid ticket type."}, status=status.HTTP_400_BAD_REQUEST)
        
        seat_group = getattr(train, seat_type + '_class_seats')

        if reservation_quantity > seat_group.quantity - seat_group.reserved:
            return Response({"detail": "Not enough seats available."}, status=status.HTTP_400_BAD_REQUEST)

        seat_group.reserved += reservation_quantity
        seat_group.save()

        seat_price = seat_group.flexible_price if ticket_type == 'flexible' else seat_group.fixed_price
        total_price = seat_price * reservation_quantity

        return Response({
            "detail": "Reservation successful for train with id {}".format(pk),
            "total_price": total_price,
            })
