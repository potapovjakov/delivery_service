from rest_framework import generics, viewsets
from api.serializers import TruckSerializer, CargoSerializer, \
    LocationSerializer, CargoDetailSerializer
from delivery.models import Truck, Cargo, Location


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class CargoDetailViewSet(generics.RetrieveUpdateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoDetailSerializer


class LocationDetailViewSet(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

