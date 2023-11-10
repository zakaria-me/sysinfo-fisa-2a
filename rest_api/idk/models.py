import time
from django.db import models
from django.core.validators import MinLengthValidator

class SeatGroup(models.Model):
    type = models.CharField(max_length=20, choices=[('first', 'First'), ('business', 'Business'), ('standard', 'Standard')])
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    fixed_price = models.FloatField(default=0.0)
    flexible_price = models.FloatField(default=0.0)


class Train(models.Model):
    """
    Each train has information about: 
    departure station
    arrival station,
    date and time,
    number of available seats and classes (First, Business or Standard).
    """
    departure_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='departure_station', null=True)
    arrival_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='arrival_station', null=True)
    departure_date = models.DateField(default=time.strftime("%Y-%m-%d"))
    departure_time = models.TimeField(null=True)
    arrival_date = models.DateField(default=time.strftime("%Y-%m-%d"))
    arrival_time = models.TimeField(null=True)

    first_class_seats = models.OneToOneField(SeatGroup, on_delete=models.CASCADE, related_name='first_class_seats', null=True)
    business_class_seats = models.OneToOneField(SeatGroup, on_delete=models.CASCADE, related_name='business_class_seats', null=True)
    standard_class_seats = models.OneToOneField(SeatGroup, on_delete=models.CASCADE, related_name='standard_class_seats', null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.first_class_seats:
                self.first_class_seats = SeatGroup.objects.create(type='first')
            if not self.business_class_seats:
                self.business_class_seats = SeatGroup.objects.create(type='business')
            if not self.standard_class_seats:
                self.standard_class_seats = SeatGroup.objects.create(type='standard')
        super().save(*args, **kwargs)
        

    @property
    def total_seats_number(self):
        return self.first_class_seats.seats + self.business_class_seats.seats + self.standard_class_seats.seats
    
    @property
    def total_reserved_seats(self):
        return self.first_class_seats.reserved + self.business_class_seats.reserved + self.standard_class_seats.reserved

    @property
    def is_full(self):
        return self.total_seats_number == self.total_reserved_seats


    def __str__(self):
        return str(self.departure_station) + " --> " + str(self.arrival_station)
    

class Station(models.Model):
    """
    Each station has information about:
    name,
    city,
    country,
    """
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)], null=True)

    def __str__(self):
        return self.name + " (" + self.city + ")"

