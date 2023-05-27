import os
import random
import string

import custom_logger
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))


logger = custom_logger.get_logger(__name__)

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
)


def csv_to_db(conn):
    """
    Импортирует локации из CSV файла в БД
    :param conn:
    :return:
    """
    table = 'delivery_location'
    file_path = os.path.join(base_dir, 'uszips.csv')
    df = pd.read_csv(file_path, converters={'zip': str})
    df = df[['zip', 'lat', 'lng', 'city', 'state_name']]
    locations = [tuple(x) for x in df.to_numpy()]
    columns = ','.join(list(df.columns)).replace('zip', 'zip_code')
    query = """INSERT INTO %s(%s)
    VALUES %%s
    ON CONFLICT (zip_code) DO NOTHING""" % (table, columns)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, locations)
        conn.commit()
        logger.info(f'{len(locations)} locations is inserted to {table}')

    except (Exception, psycopg2.DatabaseError) as error:
        logger.exception(f'Error: {error}')
        conn.rollback()
    finally:
        cursor.close()


def add_trucks(conn):
    """
    Добавляет 20 рандомных автомобилей в БД
    :param conn:
    :return:
    """
    query = """SELECT zip_code FROM delivery_location"""
    cursor = conn.cursor()
    cursor.execute(query)
    zip_codes = cursor.fetchall()

    truck_numbers = []

    def generate_truck_number():
        """
        Генерирует уникальный номер автомобиля
        :return:
        """
        integer = random.randint(1000, 9999)
        liter = random.choice(string.ascii_uppercase)
        number = f'{integer}{liter}'
        if number not in truck_numbers:
            truck_numbers.append(number)
            return number
        else:
            generate_truck_number()

    for truck in range(20):
        truck_number = generate_truck_number()
        current_location = random.choice(zip_codes)[0]
        load_capacity = random.randint(1, 1000)
        try:
            cursor.execute(
                """INSERT INTO delivery_truck (
                truck_number,
                current_location_id,
                load_capacity
                )
                VALUES (%s, %s, %s)""", (
                    truck_number,
                    current_location,
                    load_capacity
                )
            )
            logger.debug(f'Inserted truck {truck_number} to db')
        except (Exception, psycopg2.DatabaseError) as error:
            logger.exception(f'Error: {error}')
            conn.rollback()

    conn.commit()
    cursor.close()
    logger.info(f'{len(truck_numbers)} trucks inserted to db')


if __name__ == '__main__':
    csv_to_db(conn)
    add_trucks(conn)
