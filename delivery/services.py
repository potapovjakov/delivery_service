from geopy.distance import geodesic

from delivery.models import Truck


def get_all_trucks(coord_cargo: tuple) -> dict:
    """
    Возвращает отсортированный по милям словарь со всем
    транспортом вида {номер(str): расстояние до груза(float)}
    :param coord_cargo:
    :return:
    """
    all_trucks = Truck.objects.all()
    point_a = coord_cargo
    dict_trucks = dict()
    for truck in all_trucks:
        point_b = (truck.current_location.lat, truck.current_location.lng)
        distance = geodesic(point_a, point_b).miles
        dict_trucks[truck.truck_number] = distance
    sorted_tuples = sorted(dict_trucks.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict
