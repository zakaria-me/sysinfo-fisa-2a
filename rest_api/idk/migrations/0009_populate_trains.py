# Generated by Django 4.2.7 on 2023-11-10 22:16
from datetime import datetime, timedelta
import random
from django.db import migrations, transaction

def populate_train_data(apps, schema_editor):
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
    
    
    with transaction.atomic():
        Train = apps.get_model("idk", "Train")
        Station = apps.get_model("idk", "Station")
        SeatGroup = apps.get_model("idk", "SeatGroup")

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
            
            first_class_seats = SeatGroup.objects.create(type='first')
            business_class_seats = SeatGroup.objects.create(type='business')
            standard_class_seats = SeatGroup.objects.create(type='standard')


            train, created = Train.objects.get_or_create(
                departure_station_id=departure_station_id,
                arrival_station_id=arrival_station_id,
                departure_date=random_date1, departure_time=random_time1,
                arrival_date=random_date2, arrival_time=random_time2,
                first_class_seats=first_class_seats, business_class_seats=business_class_seats, standard_class_seats=standard_class_seats
            )
            if created:
                fst_price_flex = random.uniform(100.0, 200.0)
                bus_price_flex = random.uniform(50.0, 100.0)
                std_price_flex = random.uniform(20.0, 50.0)
                # First
                qty = random.randint(10, 30)
                first_class_seats.quantity = qty
                first_class_seats.flexible_price = round(fst_price_flex, 2)
                first_class_seats.fixed_price = round(fst_price_flex * 1.2, 2)
                first_class_seats.reserved = random.randint(0, int(qty * 0.8))  
                # Business
                qty = random.randint(30, 70)
                business_class_seats.quantity = qty
                business_class_seats.flexible_price = round(bus_price_flex, 2)
                business_class_seats.fixed_price = round(bus_price_flex * 1.2, 2)
                business_class_seats.reserved = random.randint(0, int(qty * 0.8))
                # Standard
                qty = random.randint(70, 150)
                standard_class_seats.quantity = qty
                standard_class_seats.flexible_price = round(std_price_flex, 2)
                standard_class_seats.fixed_price = round(std_price_flex * 1.2, 2)
                standard_class_seats.reserved = random.randint(0, int(qty * 0.8))
                
                first_class_seats.save()
                business_class_seats.save()
                standard_class_seats.save()

            

class Migration(migrations.Migration):

    dependencies = [
        ("idk", "0008_seatgroup_alter_train_business_class_seats_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_train_data),
        ]