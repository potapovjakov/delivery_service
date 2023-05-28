from delivery.models import Cargo, Location, Truck
from rest_framework import generics, viewsets

from api.serializers import (CargoDetailSerializer, CargoSerializer,
                             CargoSerializerWithoutField, LocationSerializer,
                             TruckSerializer, TruckSerializerWithoutField)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = TruckSerializerWithoutField
        return serializer_class


class CargoViewSet(generics.ListCreateAPIView):
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
        print('distance ', distance)
        if distance is None:
            distance = 450
        return {'distance': int(distance)}


class CargoDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = CargoSerializerWithoutField
        return serializer_class


class LocationDetailViewSet(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
