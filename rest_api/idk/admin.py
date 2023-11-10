from django.contrib import admin

# Register your models here.

from .models import SeatGroup, Station, Train

admin.site.register(Train)
admin.site.register(Station)
admin.site.register(SeatGroup)