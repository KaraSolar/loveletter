'''
**module: telemetry_database**

*** Exert caution when using sqlite in conjunction with Thread-based parallelism:
It is not safe to open the database in one thread and then pass the connection off
to a different thread for processing, specially using redhat.

This module defines a TelemetryDatabase class for connecting to the telemetry database
and methods to write to both of the telemetry database tables.

**Class:**

* `TelemetryDatabase(db_name:"model/telemetry.db")`: Initializes a TelemetryDatabase object
    that connects to telemetry database and can write to both tables.
    - `db_name` = "model/telemetry.db" : name of the database, leave default (str).


**Methods:**

* __init__()`: initializes the connection and verifies that the appropiate tables
    exists with the appropiate datatypes, calls methods connect_to_database(), and
    create_tables().
* `connect_to_database()`: creates the conn and cursor objects.
* `create_tables()`: verifies if tables: Trip and TelemetryData 
    exists otherwise will create them.
* `insert_trip(trip_passenger_qty:int)`: expects and integer the number of passengers
    in that trip, returns an int, the row id of the recently created trip.
* `insert_telemetry(telemetryTimeStamp:str,
                    tripId:int,
                    telemetryBatteryVoltageSystem:float,
                    telemetryBatteryCurrentSystem:float,
                    telemetryBatteryPowerSystem:int,
                    telemetryBatteryStateOfChargeSystem:int,
                    telemetryPVDCCoupledPower:int,
                    telemetryPVDCCoupledCurrent:float,
                    telemetryLatitude1:float,
                    telemetryLatitude2:float,
                    telemetryLongitude1:float,
                    telemetryLongitude2:float,
                    telemetryCourse:float,
                    telemetrySpeed:float,
                    telemetryGPSFix:int,
                    telemetryGPSNumberOfSatellites:int,
                    telemetryAltitude1:float,
                    telemetryAltitude2:float)`: writes to the TelemetryData table.

**Example:**

```python
>>> telemetry_database = TelemetryDatabase()
>>> trip_id = telemetry_database.(insert_trip=5)
'''

import sqlite3
from datetime import datetime


class TelemetryDatabase:
    '''
    as per sqlite3 api documentation: Note The context manager neither implicitly opens a new transaction nor closes the connection.
    '''
    def __init__(self, db_name: str = "model/telemetry.db"):
        self.conn, self.cursor = self.connect_to_database(db_name)
        self.create_tables()
        self.__trip_id = None
        self.timestamp = None

    def connect_to_database(self, db_name):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
        except sqlite3.Error as exc:
            raise sqlite3.Error from exc
        else:
            return conn, cursor

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Trip (
                                tripId           INTEGER PRIMARY KEY AUTOINCREMENT,
                                tripPassengerQty INTEGER NOT NULL
                                );
                                ''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS TelemetryData (
                                telemetryTimeStamp                  TEXT    PRIMARY KEY
                                                                            NOT NULL,
                                tripId                              INTEGER REFERENCES Trip (tripId),
                                telemetryBatteryVoltageSystem       REAL,
                                telemetryBatteryCurrentSystem       REAL,
                                telemetryBatteryPowerSystem         INTEGER,
                                telemetryBatteryStateOfChargeSystem INTEGER,
                                telemetryPVDCCoupledPower           INTEGER,
                                telemetryPVDCCoupledCurrent         REAL,
                                telemetryLatitude1                  INTEGER,
                                telemetryLatitude2                  INTEGER,
                                telemetryLongitude1                 INTEGER,
                                telemetryLongitude2                 INTEGER,
                                telemetryCourse                     INTEGER,
                                telemetrySpeed                      REAL,
                                telemetryGPSFix                     INTEGER,
                                telemetryGPSNumberOfSatellites      INTEGER,
                                telemetryAltitude1                  INTEGER,
                                telemetryAltitude2                  INTEGER
                            )
                            WITHOUT ROWID;
                                ''')
        except sqlite3.Error as exc:
            raise sqlite3.Error from exc
        else:
            self.conn.commit()

    def insert_trip(self, trip_passenger_qty: int) -> None:
        try:
            self.cursor.execute('''
                INSERT INTO Trip(tripPassengerQty) VALUES(?)
            ''', (trip_passenger_qty,))
            row = self.cursor.lastrowid
        except sqlite3.Error as exc:
            raise sqlite3.Error from exc
        else:
            self.conn.commit()
            self.__trip_id = row

    def insert_telemetry(self, telemetry:dict):
        self.timestamp = datetime.now().strftime("%y/%m/%d %H:%M:%S.%f")[:-3]
        try:
            self.cursor.execute('''
                INSERT INTO TelemetryData VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (self.timestamp,self.__trip_id,telemetry["battery_voltage"],
                  telemetry["battery_current"], telemetry["battery_power"],
                  telemetry["battery_state_of_charge"], telemetry["pv-dc-coupled_power"],
                  telemetry["pv-dc-coupled_current"],telemetry["latitude1"],
                  telemetry["latitude2"], telemetry["longitude1"],
                  telemetry["longitude2"], telemetry["course"], telemetry["speed"],
                  telemetry["gps_fix"], telemetry["gps_number_of_satellites"],
                  telemetry["altitude1"], telemetry["altitude2"]))
        except sqlite3.Error as exe:
            raise sqlite3.Error from exe
        else:
            self.conn.commit()

    def end_of_trip(self):
        self.__trip_id = None

    def close_connection(self) -> int:
        try:
            self.conn.close()
        except sqlite3.Error as exe:
            raise sqlite3.Error from exe
        else:
            return 1
