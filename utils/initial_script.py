import os
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv
import pandas as pd
import custom_logger



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
    table = 'delivery_location'
    file_path = os.path.join(base_dir, 'uszips.csv')
    df = pd.read_csv(file_path)
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
        logger.info(f'{len(locations)} locations is inserted to table {table}')

    except (Exception, psycopg2.DatabaseError) as error:
        logger.exception(f'Error: {error}')
        conn.rollback()
    finally:
        cursor.close()


if __name__ == '__main__':
    csv_to_db(conn)
