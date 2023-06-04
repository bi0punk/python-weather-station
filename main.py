from flask import Flask, request, render_template
import datetime
from db import get_db_connection
from gtts import gTTS
import os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_sensor_data():
    return render_template("index.html")


@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if data and 'temperature' in data:
        temperature = float(data['temperature'])
        save_sensor_data(temperature)
        check_temperature(temperature, 17.0)  # Cambia 18.0 por el valor límite que desees
        print(data)
        return str(temperature)
    else:
        return 'error'


# Función que guarda la data en la base de datos
def save_sensor_data(temperature):
    conn = get_db_connection()
    cursor = conn.cursor()
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO sensor_data (temperature, timestamp) VALUES (?, ?)", (temperature, current_datetime))
    conn.commit()
    conn.close()


# Función que busca toda la información de la base de datos
def fetch_sensor_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, temperature, timestamp FROM sensor_data")
    sensor_data = [{'id': row['id'], 'temperature': row['temperature'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]
    conn.close()
    return sensor_data


# Función que revisa si la temperatura es más baja que el límite
def check_temperature(temperature, limit):
    if temperature < limit:
        text = f"temperatura baja detectada,  {limit} grados"
        text_to_speech(text)




def text_to_speech(text, lang='es'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")  # Reproduce el archivo de audio generado


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.129", port=5000)