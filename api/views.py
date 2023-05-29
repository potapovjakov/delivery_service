from delivery.models import Cargo, Location, Truck
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CargoDetailSerializer, CargoSerializer,
                             CargoSerializerEditField, LocationSerializer,
                             TruckSerializer, TruckSerializerEditField)


class TruckViewSet(generics.ListAPIView):
    """
    Список всех машин
    """
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer


class TruckDetailViewSet(generics.RetrieveUpdateAPIView):
    """
    Детальная информация о машине по ID с возможностью
    редактировать текущее местоположение
    """
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = TruckSerializerEditField
        return serializer_class


class CargoViewSet(generics.ListCreateAPIView):
    """
    Список всех грузов
    """
    serializer_class = CargoSerializer

    def get_queryset(self):
        weight = self.request.query_params.get('weight')
        if weight:
            queryset = Cargo.objects.filter(weight__lte=weight)
        else:
            queryset = Cargo.objects.all()
        return queryset

    def get_serializer_context(self):
        distance = self.request.query_params.get('distance')
        if distance is None:
            distance = 450
        return {'distance': int(distance)}


class CargoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    Детальная информация о грузе с возможностью изменить вес и
    описание
    """
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = CargoSerializerEditField
        return serializer_class


class LocationViewSet(generics.ListAPIView):
    """
    Просмотр всех локаций
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    pagination_class = PageNumberPagination


class LocationDetailViewSet(generics.ListAPIView):
    """
    Просмотр координат локации по zip_code
    """
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
