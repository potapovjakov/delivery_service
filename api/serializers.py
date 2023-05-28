from delivery.models import Cargo, Location, Truck
from delivery.services import get_all_trucks
from rest_framework import serializers


class TruckSerializer(serializers.ModelSerializer):
    """
    Для создания записи о машине и отображения всех полей
    """
    class Meta:
        model = Truck
        depth = 1
        fields = (
            'id',
            'truck_number',
            'load_capacity',
            'current_location',
        )


class TruckSerializerWithoutField(serializers.ModelSerializer):
    """
    Позволяет редактировать только текущее месторасположение
    """
    class Meta:
        model = Truck
        fields = ('current_location',)


class CargoSerializer(serializers.ModelSerializer):
    """
    Для отображения всех полей груза и поля 'nearest_trucks'
    в котором счетчик всех машин находящихся не далее 450 миль
    """
    nearest_trucks = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_nearest_trucks_count',
    )

    class Meta:
        model = Cargo
        depth = 1

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
        dict_trucks = get_all_trucks(obj)
        count = 0
        for k, v in dict_trucks.items():
            if v <= 450:
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
        depth = 1
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


class CargoSerializerWithoutField(serializers.ModelSerializer):
    """
    Позволяет редактировать только вес и описание
    """
    class Meta:
        model = Cargo
        fields = ('weight', 'description')


class LocationSerializer(serializers.ModelSerializer):
    """
    Возвращает только широту и долготу
    """

    class Meta:
        model = Location
        fields = (
            'lat',
            'lng',
        )
