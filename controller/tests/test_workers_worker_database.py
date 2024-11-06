import pytest
import queue
from controller.workers import WorkerDatabase
import time
import sqlite3


@pytest.fixture(autouse=True)
def delete_table_rows() -> None:
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TelemetryData")
    cursor.execute("DELETE FROM Trip")
    conn.close()


@pytest.fixture(scope="function", autouse=True)
def queue_worker_database() -> queue.Queue:
    queue_worker_database = queue.Queue()
    yield queue_worker_database


@pytest.fixture(scope="function", autouse=True)
def worker_database(queue_worker_database) -> WorkerDatabase:
    worker_database = WorkerDatabase(db_name="model/test_telemetry.db",
                                     queue_worker_database=queue_worker_database)
    yield worker_database
    queue_worker_database.put({"type":"destroy"})


@pytest.fixture(scope="function", autouse=True)
def data_insert() -> dict:
    telemetry = {"battery_voltage": 999999.9, "battery_current": 0.7,
                 "battery_power": 7, "battery_state_of_charge": 7,
                 "pv-dc-coupled_power": 8, "pv-dc-coupled_current": 0.8,
                 "latitude1": 9, "latitude2": 9, "longitude1": 9,
                 "longitude2": 9, "course": 9, "speed": 0.09,
                 "gps_fix": 9, "gps_number_of_satellites": 9,
                 "altitude1": 9, "altitude2": 9}
    yield telemetry


# Refactor nested functions.
def test_telemetry_insertion(queue_worker_database, worker_database, data_insert):
    telemetry = data_insert
    queue_worker_database = queue_worker_database
    worker_database.start()
    queue_worker_database.put(item={"type": "telemetry", "value": telemetry})
    time.sleep(1)
    queue_worker_database.put(item={"type": "destroy"})
    time.sleep(4)
    assert not worker_database.is_alive()  # Only 1 thread at the time
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT telemetryBatteryVoltageSystem FROM TelemetryData ORDER BY telemetryTimeStamp DESC LIMIT 1")
    result = cursor.fetchall()
    result = result[0][0]
    assert telemetry["battery_voltage"] == result
    conn.close()


# refactor nesting.
def test_trip_insertion(queue_worker_database, worker_database):
    trip_passenger_qty = 20
    queue_worker_database = queue_worker_database
    worker_database.start()
    queue_worker_database.put(item={"type": "trip", "value": trip_passenger_qty})
    time.sleep(1)
    queue_worker_database.put(item={"type": "destroy"})
    time.sleep(4)
    assert not worker_database.is_alive()  # Only 1 thread at the time
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tripPassengerQty FROM Trip WHERE tripPassengerQty = ?", (trip_passenger_qty,))
    result = cursor.fetchall()
    result = result[0][0]
    assert trip_passenger_qty == result
    conn.close()


def test_end_trip(queue_worker_database, worker_database, data_insert):
    trip_passenger_qty = 20
    telemetry = data_insert
    queue_worker_database = queue_worker_database
    worker_database.start()
    queue_worker_database.put(item={"type": "trip", "value": trip_passenger_qty})
    queue_worker_database.put(item={"type": "telemetry", "value": telemetry})
    queue_worker_database.put(item={"type": "end_trip"})
    time.sleep(3)
    queue_worker_database.put(item={"type": "telemetry", "value": telemetry})
    time.sleep(1)
    queue_worker_database.put(item={"type": "destroy"})
    time.sleep(4)
    assert not worker_database.is_alive()  # Only 1 thread at the time
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tripId FROM TelemetryData ORDER BY telemetryTimeStamp DESC LIMIT 1")
    result = cursor.fetchall()
    result = result[0][0]
    assert result is None
    conn.close()

