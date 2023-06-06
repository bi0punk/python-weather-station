from flask import Flask, request, render_template
import datetime
from core.db import get_db_connection
from gtts import gTTS
import os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("/home/index.html", fetch_sensor_data=fetch_sensor_data)


@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    
    data = request.json
    if data is not None and 'temperature' in data:
        temperature = float(data['temperature'])
        save_sensor_data(temperature)
        check_temperature(temperature, 13.0)  # Cambia 18.0 por el valor límite que desees
        
        return str(temperature)
    else:
        return 'error'


def save_sensor_data(temperature):
    with get_db_connection() as conn:
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_data (temperature, timestamp) VALUES (?, ?)", (temperature, current_datetime))
        conn.commit()


def fetch_sensor_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, temperature, timestamp FROM sensor_data")
        sensor_data = [{'id': row['id'], 'temperature': row['temperature'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]
    return sensor_data


def check_temperature(temperature, limit):
    if temperature < limit:
        text = f"Temperatura baja detectada, {limit} grados"
        print(text)





if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.129", port=5000)
