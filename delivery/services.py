import os
import random

import psycopg2
from dotenv import load_dotenv
from geopy.distance import geodesic
from utils import custom_logger

from delivery.models import Truck

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))

logger = custom_logger.get_logger(__name__)


def get_all_trucks(obj) -> dict:
    """
    Вовращает словарь всех автомобилей с дистанцией до
    переданных в 'obj' координат
    :param obj:
    :return:
    """
    all_trucks = Truck.objects.all()
    point_a = (obj.pick_up.lat, obj.pick_up.lng)
    dict_trucks = dict()
    for truck in all_trucks:
        point_b = (truck.current_location.lat, truck.current_location.lng)
        distance = geodesic(point_a, point_b).miles
        dict_trucks[truck.truck_number] = distance
    return dict_trucks


def auto_update_tracks_location() -> None:
    """
    Функция получает из БД локации и ID всех автомобилей. Затем у автомобилей
    обновляется current_location (случайными значениями из таблицы locations)
    :return:
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    query_zip = """SELECT zip_code FROM delivery_location"""
    query_track_ids = """SELECT id FROM delivery_truck"""

    cursor = conn.cursor()
    cursor.execute(query_zip)
    zip_codes = cursor.fetchall()
    cursor.execute(query_track_ids)
    truck_ids = cursor.fetchall()
    for i in truck_ids:
        truck_id = i[0]
        new_location = random.choice(zip_codes)[0]
        try:
            cursor.execute(
                """UPDATE delivery_truck 
                SET current_location_id = %s WHERE id = %s;
                """, (new_location, truck_id)
            )
            logger.debug(f'Update truck {truck_id}')
        except (Exception, psycopg2.DatabaseError) as error:
            logger.exception(f'Error: {error}')
            conn.rollback()
    conn.commit()
    cursor.close()
    logger.debug(f'{len(truck_ids)} trucks updated')
