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
    departure_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='departure_station', null=True)
    arrival_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='arrival_station', null=True)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    seats_number = models.IntegerField()
    first_class_seats = models.IntegerField()
    business_class_seats = models.IntegerField()
    standard_class_seats = models.IntegerField()

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
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " (" + self.city + ")"

