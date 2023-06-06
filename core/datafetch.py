import sqlite3
from db import get_db_connection


def fetch_sensor_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, temperature, timestamp FROM sensor_data")
        sensor_data = [{'id': row['id'], 'temperature': row['temperature'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]
    return sensor_data
