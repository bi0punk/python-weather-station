import datetime
import csv
from flask import Flask, request, render_template
from prettytable import PrettyTable
from colorama import init, Fore, Style
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
init(autoreset=True)  # Inicializa colorama para que los colores se reseteen automáticamente

def save_to_csv(data, filename):
    with open(f'data/{filename}', 'a', newline='') as csvfile:
        fieldnames = ['Sensor', 'Temperatura (°C)', 'Humedad (%)', 'Fecha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

def save_to_db(data, table_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sensor_esp',
            user='dba_user',
            password='DB_PASSWORD_REEMPLAZAR'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = f"""INSERT INTO {table_name} (fecha, temperatura, humedad) 
                               VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, (data['Fecha'], data['Temperatura (°C)'], data['Humedad (%)']))
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

        if 'temperatura_dht22' not in data or 'humedad_dht22' not in data or 'temperatura_dht11' not in data or 'humedad_dht11' not in data:
            return 'Datos incompletos', 400  # Bad Request

        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        temperatura_dht22 = data['temperatura_dht22']
        humedad_dht22 = data['humedad_dht22']
        temperatura_dht11 = data['temperatura_dht11']
        humedad_dht11 = data['humedad_dht11']

        # Crear tablas PrettyTable para mostrar los datos
        table = PrettyTable()
        table.field_names = [Fore.BLUE + 'Sensor', Fore.BLUE + 'Temperatura (°C)', Fore.BLUE + 'Humedad (%)' + Style.RESET_ALL]
        table.add_row(['Exterior', f'{Fore.GREEN}{temperatura_dht22:.1f}', f'{Fore.GREEN}{humedad_dht22:.1f}' + Style.RESET_ALL])
        table.add_row(['Interior', f'{Fore.CYAN}{temperatura_dht11:.1f}', f'{Fore.CYAN}{humedad_dht11:.1f}' + Style.RESET_ALL])

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
        with open('data/datos_sensor_dht22.csv', 'r') as csvfile_dht22:
            reader_dht22 = csv.DictReader(csvfile_dht22)
            for row in reader_dht22:
                data_dht22.append(row)
    except FileNotFoundError:
        pass

    try:
        with open('data/datos_sensor_dht11.csv', 'r') as csvfile_dht11:
            reader_dht11 = csv.DictReader(csvfile_dht11)
            for row in reader_dht11:
                data_dht11.append(row)
    except FileNotFoundError:
        pass

    return render_template('index.html', data_dht22=data_dht22, data_dht11=data_dht11)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
