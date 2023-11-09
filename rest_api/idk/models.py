from django.db import models

# Create your models here.
class Train(models.Model):
    """
    Each train has information about: 
    departure station
    arrival station,
    date and time,
    number of available seats and classes (First, Business or Standard).
    """
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    seats_number = models.IntegerField()
    first_class_seats = models.IntegerField()
    business_class_seats = models.IntegerField()
    standard_class_seats = models.IntegerField()

    def __str__(self):
        return self.departure_station + " to " + self.arrival_station
