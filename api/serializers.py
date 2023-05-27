from delivery.models import Truck, Cargo, Location
from rest_framework import serializers
from delivery.services import get_all_trucks


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
    nearest_trucks = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_nearest_trucks_count',
    )

    class Meta:
        model = Cargo
        fields = (
            'id',
            'pick_up',
            'delivery',
            'weight',
            'created_at',
            'updated_at',
            'description',
            'nearest_trucks'
        )

    def get_nearest_trucks_count(self, obj) -> int:
        """
        Возвращает количество машин, находящихся
        не далее чем в 450 милях от точки загрузки
        :param obj:
        :return:
        """
        dict_trucks = get_all_trucks(Location, obj)
        count = 0
        for k, v in dict_trucks.items():
            if v <= 450:
                count += 1

        return count


class CargoDetailSerializer(serializers.ModelSerializer):
    all_trucks = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_all_trucks',
    )
    class Meta:
        model = Cargo
        fields = (
            'id',
            'pick_up',
            'delivery',
            'weight',
            'created_at',
            'updated_at',
            'description',
            'all_trucks'
        )

    def get_all_trucks(self, obj) -> dict:
        """
        Возвращает словарь со всеми машинами отсортированный по
        увеличению расстояния до места загрузки
        :param obj:
        :return:
        """
        dict_trucks = get_all_trucks(Location, obj)
        sorted_tuples = sorted(dict_trucks.items(), key=lambda item: item[1])
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'lat',
            'lng',
        )
