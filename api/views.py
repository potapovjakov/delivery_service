from rest_framework import generics, viewsets
from api.serializers import TruckSerializer, CargoSerializer, \
    LocationSerializer, CargoDetailSerializer, CargoSerializerWithoutField, \
    TruckSerializerWithoutField
from delivery.models import Truck, Cargo, Location


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


class CargoDetailViewSet(generics.RetrieveUpdateAPIView):
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
