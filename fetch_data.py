import sqlite3

def consultar_datos():
    conn = sqlite3.connect('sensor_data.db')  # Reemplaza con la ruta correcta de tu base de datos SQLite
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data")
    datos = cursor.fetchall()

    for fila in datos:
        print(fila)  # O realiza alguna operación con los datos

    conn.close()