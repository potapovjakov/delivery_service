from django.shortcuts import get_object_or_404
from geopy.distance import geodesic
from delivery.models import Truck


def get_all_trucks(model, obj) -> dict:
    all_trucks = Truck.objects.all()
    coord_a = get_object_or_404(
        model,
        pk=obj.pick_up
    )
    point_a = (coord_a.lat, coord_a.lng)
    dict_trucks = dict()
    for truck in all_trucks:
        coord_b = get_object_or_404(
            model,
            pk=truck.current_location
        )
        point_b = (coord_b.lat, coord_b.lng)
        distance = geodesic(point_a, point_b).miles
        dict_trucks[truck.truck_number] = distance
    return dict_trucks
