from django.shortcuts import get_object_or_404
from geopy.distance import geodesic

from delivery.models import Location, Truck


def get_all_trucks(obj) -> dict:
    all_trucks = Truck.objects.all()
    point_a = (obj.pick_up.lat, obj.pick_up.lng)
    dict_trucks = dict()
    for truck in all_trucks:
        point_b = (truck.current_location.lat, truck.current_location.lng)
        distance = geodesic(point_a, point_b).miles
        dict_trucks[truck.truck_number] = distance
    return dict_trucks
