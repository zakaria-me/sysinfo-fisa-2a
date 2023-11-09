from django.contrib import admin

# Register your models here.

from .models import Station, Train

admin.site.register(Train)
admin.site.register(Station)