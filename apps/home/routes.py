from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
import datetime
import sqlite3

database = 'sensor_data.db'


def get_db_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

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
        sensor_data = [{'id': row['id'], 'temperature': row['temperature'], 'timestamp': row['timestamp']}
                        for row in cursor.fetchall()]
    return sensor_data


@blueprint.route('/ultimos100')
@login_required
def obtener_ultimos_registros():
    registros = fetch_sensor_data()
    ultimos_registros = registros[-100:]
    return jsonify(ultimos_registros)


def check_temperature(temperature, limit):
    if temperature < limit:
        text = f"Temperatura baja detectada, {limit} grados"
        print(text)


@blueprint.route('/index')
@login_required
def index():
    ultimo = fetch_sensor_data()[-1]
    temperature = ultimo.get('temperature')
    date_event = ultimo.get('timestamp')

    print(obtener_ultimos_registros)
    return render_template('home/index.html', segment='index', temperature=temperature, date_event=date_event)

@blueprint.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if data is not None and 'temperature' in data:
        temperature = float(data['temperature'])
        print(temperature)
        save_sensor_data(temperature)
        check_temperature(temperature, 13.0)  # Cambia 18.0 por el valor límite que desees
        rounded = round(temperature)
        print(f'El valor aproximado es {rounded}')
        print(rounded)  # Salida: 4
        return str(temperature)
    else:
        return 'error'

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except Exception:
        return None
