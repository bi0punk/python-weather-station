import pytest

import app
import routes


def test_datos_sensor_incomplete_returns_400():
    client = app.app.test_client()
    resp = client.post("/datos_sensor/", json={"temperatura_dht22": 20.0})
    assert resp.status_code == 400


def test_index_renders_without_csv():
    client = app.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200


def test_save_to_db_rejects_unknown_table():
    data = {"Fecha": "x", "Temperatura (°C)": 1, "Humedad (%)": 1}
    with pytest.raises(ValueError, match="Tabla no permitida"):
        app.save_to_db(data, "otra_tabla")