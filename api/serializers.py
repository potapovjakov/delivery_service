from delivery.models import Truck, Cargo
from rest_framework import serializers


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = (
            'id',
            'truck_number',
            'load_capacity',
            'current_location',
        )


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            'id',
            'pick_up',
            'delivery',
            'weight',
            'created_at',
            'updated_at',
            'description'
        )
