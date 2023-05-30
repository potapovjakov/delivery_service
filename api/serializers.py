from delivery.models import Cargo, Location, Truck
from delivery.services import get_all_trucks
from rest_framework import serializers


class TruckSerializer(serializers.ModelSerializer):
    """Просмотр всех машин"""
    class Meta:
        model = Truck
        fields = (
            'id',
            'truck_number',
            'load_capacity',
            'current_location',
        )


class TruckSerializerEditField(serializers.ModelSerializer):
    """Позволяет редактировать только текущее месторасположение"""
    class Meta:
        model = Truck
        fields = ('current_location',)


class CargoSerializer(serializers.ModelSerializer):
    """
    Для отображения всех полей груза и поля 'nearest_trucks'
    в котором счетчик всех машин находящихся не далее 450
    миль (либо количества миль переданного в url параметре 'distance')
    Груз можно отфильтровать по весу переданном в url параметре 'weight'
    """
    nearest_trucks = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_nearest_trucks_count',
    )

    def get_context_distance(self, obj) -> int:
        return self.context.get('distance')

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
            'nearest_trucks',
        )

    def get_nearest_trucks_count(self, obj) -> int:
        """
        Возвращает количество машин, находящихся
        не далее чем в 450 милях (либо количество миль переданных в url
         параметре 'distance') от точки загрузки
        :param obj:
        :return:
        """
        dict_trucks = get_all_trucks(obj)
        distance = self.get_context_distance(obj)
        count = 0
        for k, v in dict_trucks.items():
            if v <= distance:
                count += 1
        return count


class CargoDetailSerializer(serializers.ModelSerializer):
    """
    Детальная информация о грузе и поле 'all_trucks'
    в котором список из номеров всех машин и расстоянием до места загрузки
    """
    all_trucks = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_all_trucks',
    )

    def get_all_trucks(self, obj) -> dict:
        """
        Возвращает словарь со всеми машинами отсортированный по
        увеличению расстояния до места загрузки
        :param obj:
        :return:
        """
        dict_trucks = get_all_trucks(obj)
        sorted_tuples = sorted(dict_trucks.items(), key=lambda item: item[1])
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict

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
            'all_trucks',
        )


class CargoSerializerEditField(serializers.ModelSerializer):
    """Позволяет редактировать только вес и описание"""
    class Meta:
        model = Cargo
        fields = (
            'weight',
            'description',
        )


class LocationSerializer(serializers.ModelSerializer):
    """Возвращает все локации"""

    class Meta:
        model = Location
        fields = '__all__'
