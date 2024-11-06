import pytest
from model.telemetry_database import TelemetryDatabase
from unittest.mock import patch
import sqlite3


@pytest.fixture(scope="function", autouse=True)
def telemetry_database_object() -> TelemetryDatabase:
    telemetry_database = TelemetryDatabase(db_name="model/test_telemetry.db")
    yield telemetry_database
    telemetry_database.close_connection()


def test_getters_setters():
    with pytest.raises(ValueError):
        TelemetryDatabase(db_name=" model/test_telemetry.db")
    with pytest.raises(ValueError):
        TelemetryDatabase(db_name="cat")
    telemetry_database = TelemetryDatabase(db_name="model/test_telemetry.db")
    assert telemetry_database._db_name == "model/test_telemetry.db"
    telemetry_database.close_connection()


def test_init_method(telemetry_database_object):
    telemetry_database_object.db_name = "model/test_telemetry.db"
    assert type(telemetry_database_object._TelemetryDatabase__conn) == sqlite3.Connection
    assert type(telemetry_database_object._TelemetryDatabase__cursor) == sqlite3.Cursor
    assert telemetry_database_object._TelemetryDatabase__trip_id is None
    assert telemetry_database_object._TelemetryDatabase__timestamp is None


def connect_mock(*args, **kwargs):
    raise sqlite3.Error("Connection failed")


def test_connect_to_database(telemetry_database_object):
    """
    mock failed connection.
    """
    with patch('sqlite3.connect', side_effect=connect_mock):
        with pytest.raises(sqlite3.Error):
            telemetry_database_object.connect_to_database("any.db")
    with patch('sqlite3.connect', side_effect=connect_mock):
        with pytest.raises(sqlite3.Error):
            telemetry_database_object.connect_to_database("cat")


def test_create_tables(telemetry_database_object):
    """
    Independent of each other test. You can delete the test_telemetry database and skip every other test
    and test independently.
    """
    telemetry_database_object.close_connection()
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info(Trip)")
    schema_info = cursor.fetchall()
    trip_table_schema = [(0, 'tripId', 'INTEGER', 0, None, 1), (1, 'tripPassengerQty', 'INTEGER', 1, None, 0)]
    assert schema_info == trip_table_schema
    cursor.execute(f"PRAGMA table_info(TelemetryData)")
    schema_info = cursor.fetchall()
    telemetry_table_schema = [(0, 'telemetryId', 'INTEGER', 0, None, 1),
                              (1, 'telemetryTimeStamp', 'TEXT', 1, None, 0),
                              (2, 'tripId', 'INTEGER', 0, None, 0),
                              (3, 'telemetryBatteryVoltageSystem', 'REAL', 0, None, 0),
                              (4, 'telemetryBatteryCurrentSystem', 'REAL', 0, None, 0),
                              (5, 'telemetryBatteryPowerSystem', 'INTEGER', 0, None, 0),
                              (6, 'telemetryBatteryStateOfChargeSystem', 'INTEGER', 0, None, 0),
                              (7, 'telemetryPVDCCoupledPower', 'INTEGER', 0, None, 0),
                              (8, 'telemetryPVDCCoupledCurrent', 'REAL', 0, None, 0),
                              (9, 'telemetryLatitude1', 'INTEGER', 0, None, 0),
                              (10, 'telemetryLatitude2', 'INTEGER', 0, None, 0),
                              (11, 'telemetryLongitude1', 'INTEGER', 0, None, 0),
                              (12, 'telemetryLongitude2', 'INTEGER', 0, None, 0),
                              (13, 'telemetryCourse', 'INTEGER', 0, None, 0),
                              (14, 'telemetrySpeed', 'REAL', 0, None, 0),
                              (15, 'telemetryGPSFix', 'INTEGER', 0, None, 0),
                              (16, 'telemetryGPSNumberOfSatellites', 'INTEGER', 0, None, 0),
                              (17, 'telemetryAltitude1', 'INTEGER', 0, None, 0),
                              (18, 'telemetryAltitude2', 'INTEGER', 0, None, 0)]
    assert schema_info == telemetry_table_schema
    conn.close()


def test_insert_non_valid_trip(telemetry_database_object):
    with pytest.raises(ValueError):
        telemetry_database_object.insert_trip(None)
    with pytest.raises(ValueError):
        telemetry_database_object.insert_trip(30)
    with pytest.raises(ValueError):
        telemetry_database_object.insert_trip(-1)
    with pytest.raises(ValueError):
        telemetry_database_object.insert_trip(2.8)
    with pytest.raises(ValueError):
        telemetry_database_object.insert_trip("cat")


def test_insert_trip(telemetry_database_object):
    """
    Also independent of every other test.
    """
    passenger_number = 5
    telemetry_database_object.insert_trip(passenger_number)
    telemetry_database_object.close_connection()
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tripPassengerQty FROM Trip WHERE tripId = (SELECT MAX(tripId) FROM Trip)")
    query = cursor.fetchall()
    query = query[0][0]
    assert passenger_number == query
    conn.close()


def test_insert_non_valid_telemetry(telemetry_database_object):
    telemetry_values = [100, -2536, 32767, 20, 20, 0, 0, 0, 0, 0, 0, 10000, 12, 12, 12, 12]
    cat_dictionary = {}
    for _ in range(16):
        cat_dictionary[f"cat{_}"] = _
    with pytest.raises(TypeError):
        telemetry_database_object.insert_telemetry(None)
    with pytest.raises(TypeError):
        telemetry_database_object.insert_telemetry(telemetry_values)
    with pytest.raises(KeyError):
        telemetry_database_object.insert_telemetry(cat_dictionary)


def test_insert_telemetry(telemetry_database_object):
    telemetry = {"battery_voltage": 0.7, "battery_current": 0.7,
                 "battery_power": 7, "battery_state_of_charge": 7,
                 "pv-dc-coupled_power": 8, "pv-dc-coupled_current": 0.8,
                 "latitude1": 9, "latitude2": 9, "longitude1": 9,
                 "longitude2": 9, "course": 9, "speed": 0.09,
                 "gps_fix": 9, "gps_number_of_satellites": 9,
                 "altitude1": 9, "altitude2": 9}
    telemetry_database_object.insert_telemetry(telemetry)
    telemetry_database_object.close_connection()
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    query = '''SELECT telemetryBatteryVoltageSystem 
    FROM TelemetryData
    WHERE telemetryId = (SELECT MAX(telemetryId)
                         FROM TelemetryData)'''
    cursor.execute(query)
    result = cursor.fetchall()
    result = result[0][0]
    assert telemetry["battery_voltage"] == result
    conn.close()


# Nesting some functions here.
def test_trip_mode_telemetry(telemetry_database_object):
    """
    Integration test.
    """
    passenger_number = 9
    telemetry_database_object.insert_trip(passenger_number)
    telemetry = {"battery_voltage": 0.7, "battery_current": 0.7,
                 "battery_power": 7, "battery_state_of_charge": 7,
                 "pv-dc-coupled_power": 8, "pv-dc-coupled_current": 0.8,
                 "latitude1": 9, "latitude2": 9, "longitude1": 9,
                 "longitude2": 9, "course": 9, "speed": 0.09,
                 "gps_fix": 9, "gps_number_of_satellites": 9,
                 "altitude1": 9, "altitude2": 9}
    telemetry_database_object.insert_telemetry(telemetry) # replaced with a for loop.
    telemetry_database_object.insert_telemetry(telemetry)
    telemetry_database_object.insert_telemetry(telemetry)
    telemetry_database_object.insert_telemetry(telemetry)
    telemetry_database_object.close_connection()
    conn = sqlite3.connect("model/test_telemetry.db") # this can be a function.
    cursor = conn.cursor()
    cursor.execute("SELECT tripPassengerQty, tripId FROM Trip WHERE tripId = (SELECT MAX(tripId) FROM Trip)")
    result_trip = cursor.fetchall()
    pass_qty = result_trip[0][0]
    trip_id_trip = result_trip[0][1]
    cursor.execute(
        "SELECT telemetryBatteryCurrentSystem, tripId FROM TelemetryData WHERE telemetryId = (SELECT MAX(telemetryId) FROM TelemetryData)")
    result_telemetry = cursor.fetchall()
    battery_current = result_telemetry[0][0]
    trip_id_telemetry = result_telemetry[0][1]
    assert pass_qty == passenger_number
    assert battery_current == telemetry["battery_current"]
    assert trip_id_trip == trip_id_telemetry
    conn.close()


def test_end_of_trip(telemetry_database_object):
    """
    Integration test.
    """
    telemetry = {"battery_voltage": 0.7, "battery_current": 0.7,
                 "battery_power": 7, "battery_state_of_charge": 7,
                 "pv-dc-coupled_power": 8, "pv-dc-coupled_current": 0.8,
                 "latitude1": 9, "latitude2": 9, "longitude1": 9,
                 "longitude2": 9, "course": 9, "speed": 0.09,
                 "gps_fix": 9, "gps_number_of_satellites": 9,
                 "altitude1": 9, "altitude2": 9}
    passenger_number = 20
    assert telemetry_database_object._TelemetryDatabase__trip_id is None
    telemetry_database_object.insert_trip(passenger_number)
    assert telemetry_database_object._TelemetryDatabase__trip_id is not None
    telemetry_database_object.end_of_trip()
    assert telemetry_database_object._TelemetryDatabase__trip_id is None
    telemetry_database_object.insert_telemetry(telemetry)
    conn = sqlite3.connect("model/test_telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tripId FROM TelemetryData WHERE telemetryId = (SELECT MAX(telemetryId) FROM TelemetryData)")
    result_telemetry = cursor.fetchall()
    trip_id_telemetry = result_telemetry[0][0]
    assert trip_id_telemetry is None
    conn.close()


def test_close_connection(telemetry_database_object):
    assert telemetry_database_object.close_connection() == 0

