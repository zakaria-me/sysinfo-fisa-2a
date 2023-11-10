from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("idk", "0006_populate_stations"),
    ]

    operations = [
         migrations.RemoveField(
            model_name="train",
            name="seats_number",
        ),
    ]
