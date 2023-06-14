from apps.home import blueprint
from flask import render_template, request
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
    conn = get_db_connection()
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (temperature, timestamp) VALUES (?, ?)", (temperature, current_datetime))
    conn.commit()
    conn.close()

def fetch_sensor_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, temperature, timestamp FROM sensor_data")
    sensor_data = [{'id': row['id'], 'temperature': row['temperature'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]
    conn.close()
    return sensor_data

def obtener_temperatura_minima():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temperature FROM sensor_data WHERE temperature = (SELECT MIN(temperature) FROM sensor_data)")
    temperatura_minima = cursor.fetchone()[0]
    aaaaaa = (cursor.fetchall)
    conn.close()
    return temperatura_minima, aaaaaa


@blueprint.route('/index')
@login_required
def index():
    ultimo = fetch_sensor_data()[-1]
    temperature = ultimo.get('temperature')
    date_event = ultimo.get('timestamp')
    minima_temp = (obtener_temperatura_minima())
    print(minima_temp)

    return render_template('home/index.html', segment='index', temperature=temperature, date_event=date_event, minima_temp = minima_temp)















@blueprint.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if data is not None and 'temperature' in data:
        temperature = float(data['temperature'])
        save_sensor_data(temperature)
        rounded = round(temperature)
        print(f'El valor aproximado es {rounded}')
        print(rounded)
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
