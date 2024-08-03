# Proyecto Flask de Monitoreo de Sensores

Este proyecto es una aplicación web basada en Flask que recibe datos de sensores de temperatura y humedad (DHT22 y DHT11) a través de solicitudes POST, los muestra en la consola utilizando PrettyTable, y guarda los datos en una base de datos MySQL. En caso de fallo en la base de datos, los datos se almacenan en archivos CSV.

## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación Flask.
- `templates/index.html`: Plantilla HTML para mostrar los datos de los sensores.
- `data/`: Carpeta que contiene los archivos CSV de respaldo.

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual y activa:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura la base de datos MySQL:
    - Crea una base de datos llamada `sensor_esp`.
    - Crea dos tablas `datos_sensor_dht22` y `datos_sensor_dht11` con las siguientes columnas:
      ```sql
      CREATE TABLE datos_sensor_dht22 (
          id INT AUTO_INCREMENT PRIMARY KEY,
          fecha DATETIME,
          temperatura FLOAT,
          humedad FLOAT
      );

      CREATE TABLE datos_sensor_dht11 (
          id INT AUTO_INCREMENT PRIMARY KEY,
          fecha DATETIME,
          temperatura FLOAT,
          humedad FLOAT
      );
      ```

5. Configura las credenciales de la base de datos en `app.py`:
    ```python
    connection = mysql.connector.connect(
        host='localhost',
        database='sensor_esp',
        user='tu_usuario',
        password='tu_contraseña'
    )
    ```

## Ejecución

1. Inicia la aplicación:
    ```bash
    python app.py
    ```

2. La aplicación estará disponible en `http://localhost:8000`.

## Uso

- Envía datos de los sensores a la ruta `/datos_sensor/` utilizando una solicitud POST con el siguiente formato JSON:
    ```json
    {
        "temperatura_dht22": 25.0,
        "humedad_dht22": 60.0,
        "temperatura_dht11": 23.0,
        "humedad_dht11": 55.0
    }
    ```

- Visita la página principal para ver los datos almacenados en `http://localhost:8000`.

## Dependencias

- Flask
- PrettyTable
- Colorama
- MySQL Connector
- CSV

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.
