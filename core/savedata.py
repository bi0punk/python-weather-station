import sqlite3
from db import get_db_connection
import datetime



def save_sensor_data(temperature):
    with get_db_connection() as conn:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_data (temperature, timestamp) VALUES (?, ?)", (temperature, current_datetime))
        conn.commit()
