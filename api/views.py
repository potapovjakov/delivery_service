from delivery.models import Cargo, Location, Truck
from rest_framework import generics, viewsets

from api.serializers import (CargoDetailSerializer, CargoSerializer,
                             CargoSerializerWithoutField, LocationSerializer,
                             TruckSerializer, TruckSerializerWithoutField)
from delivery.services import get_all_trucks


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = TruckSerializerWithoutField
        return serializer_class


class CargoViewSet(generics.ListCreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    # def get_queryset(self):
    #     weight = self.request.query_params.get('weight', default=None)
    #     if weight:
    #         queryset = Cargo.objects.filter(weight__lte=weight)
    #     else:
    #         queryset = Cargo.objects.all()
    #     return queryset
    #
    # def get_nearest_trucks_count(self, coordinates) -> int:
    #     """
    #     Возвращает количество машин, находящихся
    #     не далее чем в 450 милях от точки загрузки,
    #     или на расстоянии, переданном в url параметре 'distance'
    #     :return:
    #     """
    #     distance = self.request.query_params.get('distance', default=450)
    #     point_a = (coordinates.pick_up.lat, coordinates.pick_up.lng)
    #     dict_trucks = get_all_trucks(point_a)
    #     count = 0
    #     for k, v in dict_trucks.items():
    #         if v <= int(distance):
    #             count += 1
    #     return count
    #
    # def get_serializer_context(self):
    #     queryset = self.get_queryset()
    #     print(queryset)
    #     for coord in queryset:
    #         count = self.get_nearest_trucks_count(coord)
    #         return {
    #             'count': count
    #         }


class CargoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = CargoSerializerWithoutField
        return serializer_class

    def get_serializer_context(self):
        coordinates = self.get_object()
        point_a = (coordinates.pick_up.lat, coordinates.pick_up.lng)
        return {
            "all_trucks_dict": get_all_trucks(point_a)
        }


class LocationDetailViewSet(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
