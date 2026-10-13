import csv
import datetime
import os

import mysql.connector
from colorama import Fore, Style, init
from flask import Flask, render_template, request
from mysql.connector import Error
from prettytable import PrettyTable

app = Flask(__name__)
init(autoreset=True)  # Inicializa colorama para que los colores se reseteen automáticamente

INSERT_QUERIES = {
    'datos_sensor_dht11': (
        "INSERT INTO datos_sensor_dht11 (fecha, temperatura, humedad) "
        "VALUES (%s, %s, %s)"
    ),
    'datos_sensor_dht22': (
        "INSERT INTO datos_sensor_dht22 (fecha, temperatura, humedad) "
        "VALUES (%s, %s, %s)"
    ),
}

def save_to_csv(data, filename):
    with open(f'data/{filename}', 'a', newline='') as csvfile:
        fieldnames = ['Sensor', 'Temperatura (°C)', 'Humedad (%)', 'Fecha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

def save_to_db(data, table_name):
    if table_name not in INSERT_QUERIES:
        raise ValueError(f"Tabla no permitida: {table_name}")
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'sensor_esp'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(INSERT_QUERIES[table_name], (data['Fecha'], data['Temperatura (°C)'], data['Humedad (%)']))
            connection.commit()
            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False

@app.route('/datos_sensor/', methods=['POST'])
def datos_sensor():
    if request.method == 'POST':
        data = request.json
        print(data)

        required = ('temperatura_dht22', 'humedad_dht22', 'temperatura_dht11', 'humedad_dht11')
        if any(key not in data for key in required):
            return 'Datos incompletos', 400  # Bad Request

        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        temperatura_dht22 = data['temperatura_dht22']
        humedad_dht22 = data['humedad_dht22']
        temperatura_dht11 = data['temperatura_dht11']
        humedad_dht11 = data['humedad_dht11']

        # Crear tablas PrettyTable para mostrar los datos
        table = PrettyTable()
        table.field_names = [
            Fore.BLUE + 'Sensor',
            Fore.BLUE + 'Temperatura (°C)',
            Fore.BLUE + 'Humedad (%)' + Style.RESET_ALL,
        ]
        table.add_row(
            'Exterior',
            f'{Fore.GREEN}{temperatura_dht22:.1f}',
            f'{Fore.GREEN}{humedad_dht22:.1f}' + Style.RESET_ALL,
        )
        table.add_row(
            'Interior',
            f'{Fore.CYAN}{temperatura_dht11:.1f}',
            f'{Fore.CYAN}{humedad_dht11:.1f}' + Style.RESET_ALL,
        )

        # Mostrar la tabla en la consola
        print(table)

        # Datos a guardar
        data_dht22 = {
            'Sensor': 'Exterior',
            'Temperatura (°C)': temperatura_dht22,
            'Humedad (%)': humedad_dht22,
            'Fecha': fecha_hora_formateada
        }

        data_dht11 = {
            'Sensor': 'Interior',
            'Temperatura (°C)': temperatura_dht11,
            'Humedad (%)': humedad_dht11,
            'Fecha': fecha_hora_formateada
        }

        # Intentar guardar en la base de datos, si falla guardar en CSV
        if not save_to_db(data_dht22, 'datos_sensor_dht22'):
            save_to_csv(data_dht22, 'datos_sensor_dht22_backup.csv')

        if not save_to_db(data_dht11, 'datos_sensor_dht11'):
            save_to_csv(data_dht11, 'datos_sensor_dht11_backup.csv')

        return 'Datos recibidos y almacenados con éxito.'

@app.route('/')
def index():
    # Leer datos del archivo CSV
    data_dht22 = []
    data_dht11 = []

    try:
        with open('data/datos_sensor_dht22.csv') as csvfile_dht22:
            reader_dht22 = csv.DictReader(csvfile_dht22)
            for row in reader_dht22:
                data_dht22.append(row)
    except FileNotFoundError:
        pass

    try:
        with open('data/datos_sensor_dht11.csv') as csvfile_dht11:
            reader_dht11 = csv.DictReader(csvfile_dht11)
            for row in reader_dht11:
                data_dht11.append(row)
    except FileNotFoundError:
        pass

    return render_template('index.html', data_dht22=data_dht22, data_dht11=data_dht11)

if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '127.0.0.1'),
        port=int(os.getenv('PORT', '8000')),
        debug=os.getenv('DEBUG', 'false').lower() == 'true',
    )
