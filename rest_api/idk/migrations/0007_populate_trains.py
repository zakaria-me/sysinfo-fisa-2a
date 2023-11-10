from datetime import datetime, timedelta
import random
from django.db import migrations, transaction

def random_date(start_date=datetime(2022, 1, 1), end_date=datetime(2024, 12, 31)):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def get_random_hours(start_hour="6:00", end_hour="23:59", max_hour_difference=4):
    start_time = datetime.strptime(start_hour, '%H:%M')
    end_time = datetime.strptime(end_hour, '%H:%M')

    random_hour = random.randint(start_time.hour, end_time.hour)
    random_minute = random.randint(0, 59)
    hour1 = datetime.strptime(f"{random_hour:02d}:{random_minute:02d}", '%H:%M')

    max_time_difference = max_hour_difference * 60
    random_minutes = random.randint(15, max_time_difference)
    hour2 = hour1 + timedelta(minutes=random_minutes)
    return hour1.time(), hour2.time()

def populate_train_data(apps, schema_editor):
        with transaction.atomic():
            Train = apps.get_model("idk", "Train")
            Station = apps.get_model("idk", "Station")
            stations_id_list = Station.objects.values_list('id', flat=True)
            station_count = len(stations_id_list)
            # Create 10000 random trains
            for i in range(10000):
                departure_station_id = stations_id_list[random.randint(1, station_count-1)]
                arrival_station_id = stations_id_list[random.randint(1, station_count-1)]
                random_date1 = random_date()
                random_time1, random_time2 = get_random_hours()
                # random_date 2 is random_date1 + 1 day if random_time2 < random_time1
                random_date2 = random_date1 if random_time2 > random_time1 else random_date1 + timedelta(days=1)
                
                fst_nb = random.randint(10, 30)
                bsn_nb = random.randint(30, 70)
                std_nb = random.randint(80, 130)
                
                Train.objects.create(
                    departure_station_id=departure_station_id,
                    arrival_station_id=arrival_station_id,
                    departure_date=random_date1,
                    departure_time=random_time1,
                    arrival_date=random_date2,
                    arrival_time=random_time2,
                    first_class_seats=fst_nb,
                    business_class_seats=bsn_nb,
                    standard_class_seats=std_nb,
                )

class Migration(migrations.Migration):

    dependencies = [
        ("idk", "0006_populate_stations"),
    ]

    operations = [
         migrations.RemoveField(
            model_name="train",
            name="seats_number",
        ),
        migrations.RunPython(populate_train_data),
    ]
