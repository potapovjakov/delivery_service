from rest_framework import generics, status, viewsets
from api.serializers import TruckSerializer, CargoSerializer
from delivery.models import Truck, Cargo
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

