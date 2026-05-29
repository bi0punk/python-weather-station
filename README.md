# arduino-python

Temperature and humidity monitoring system. A Wemos R1 D1 board with a DHT22 sensor serves JSON data via an internal HTTP endpoint. A Flask app polls the data, stores it in SQLite, and displays it in a web template.

## Stack

Python 3, Flask, Arduino/C++ (Wemos R1 D1), DHT22 sensor, SQLite

## Components

- Arduino/Wemos firmware serves sensor data as JSON
- Flask app polls the Arduino endpoint
- Data stored in SQLite with min/max tracking
- Bootstrap web UI for visualization

## Usage

1. Flash the Wemos board with the sensor firmware
2. Run the Flask app:
```bash
pip install flask
python app.py
```

## License

MIT
