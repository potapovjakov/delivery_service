from django.contrib import admin

from .models import Cargo, Location, Truck


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'zip_code',
        'city',
        'state_name',
        'lng',
        'lat',
    )
    search_fields = (
        'zip_code',
    )


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'pick_up',
        'delivery',
        'weight',
        'created_at',
        'updated_at',
        'description',
    )


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = (
        'truck_number',
        'current_location',
        'load_capacity',
    )
