"""
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
"""

import sqlite3
from datetime import datetime
import re


class TelemetryDatabase:
    """
    As per sqlite3 api documentation: Note The context manager neither implicitly opens a new
    transaction nor closes the connection.
    """
    def __init__(self, db_name: str,
                 passenger_number_config: dict, trip_purposes_config: list):
        """
        Instantiate the connection to the database and create the tables.
        :param db_name: str expects a string constraint to "model/telemetry.db",
        "model/dev_telemetry.db", "model/test_telemetry.db" won't admit other values
        """
        self.db_name = db_name
        self.passenger_number_config = passenger_number_config
        self.trip_purposes_config = trip_purposes_config
        self.__conn, self.__cursor = self.connect_to_database(self.db_name)
        self.create_tables()
        self.__trip_id = None
        self.__timestamp = None

    @property  # Getter
    def db_name(self) -> str:
        """Get the db name."""
        return self._db_name

    @db_name.setter  # Setter
    def db_name(self, db_name: str) -> None:
        """Set the database name.
        Args:
            db_name (str): The IP address to set.
        Raises:
            ValueError: If the database name is invalid.
        """
        pattern = r"model/\d{4}_\d{2}_\d{2}_telemetry.db|model/dev_telemetry.db|model/test_telemetry.db"
        if not re.search(pattern=pattern, string=db_name):
            raise ValueError("Not a valid database.")
        self._db_name = db_name

    def connect_to_database(self, db_name):
        """
        Connects to the database.
        :param db_name: str the database name.
        :return: conn and cursor
        :raises: sqlite3.Error if encounters an error when connecting to the database.
        """
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
        except sqlite3.Error as exc:
            self.close_connection()
            raise sqlite3.Error from exc
        else:
            return conn, cursor

    def create_tables(self) -> None:
        """
        creates the Trip and TelemetryData tables IF NOT EXISTS, refer to the method or the
        database itself for the schema.
        :raises: sqlite3.Error if encounters an error when committing the changes
        """
        try:
            self.__cursor.execute('''CREATE TABLE IF NOT EXISTS Trip (
                                tripId           INTEGER PRIMARY KEY AUTOINCREMENT,
                                tripPassengerQty INTEGER NOT NULL,
                                tripPurpose      TEXT    NOT NULL
                                );
                                ''')

            self.__cursor.execute('''CREATE TABLE IF NOT EXISTS TelemetryData (
                                    telemetryId                         INTEGER PRIMARY KEY AUTOINCREMENT,
                                    telemetryTimeStamp                  TEXT    NOT NULL,
                                    tripId                              INTEGER,
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
                                    telemetryAltitude2                  INTEGER,
                                    FOREIGN KEY (tripId) REFERENCES Trip (tripId)
                                );''')
        except sqlite3.Error as exc:
            self.close_connection()
            raise sqlite3.Error from exc
        else:
            self.__conn.commit()

    def trip_insert_values_validation(self, trip_passenger_qty, trip_purpose):
        """
        Validates fields for trip insertion.
        :param trip_passenger_qty: dict greater than 0 but lower than config file, required.
        :param trip_purpose: str must be one of the values defined in config.yml
        :return: None
        :raises: ValueError if passenger None, less than or higher than config file.
        """
        if trip_passenger_qty is None:
            raise ValueError("passenger can't be NULL")
        if not isinstance(trip_passenger_qty, int):
            raise ValueError("passenger must be int.")
        if (trip_passenger_qty > self.passenger_number_config["max"]
                or trip_passenger_qty < self.passenger_number_config["min"]):
            raise ValueError("passengers not in range")
        if trip_purpose not in self.trip_purposes_config:
            raise ValueError("trip purpose not correct")

    def insert_trip(self, value: dict) -> None:
        """
        Inserts a new trip row to the Trip table with the number of passengers given.
        When successful assigns the attribute trip_id to the trip id.
        :param value: dict that contains passenger quantity and the trip purpose.
        :param value: dict
        :return: None
        :raises: ValueError if passenger None, less than or higher than config file.
        :raises: sqlite3.Error if database error.
        """
        trip_passenger_qty, trip_purpose = value.values()
        self.trip_insert_values_validation(trip_passenger_qty=trip_passenger_qty, trip_purpose=trip_purpose)
        try:
            self.__cursor.execute('''
                INSERT INTO Trip(tripPassengerQty, tripPurpose) VALUES(?,?)
            ''', (trip_passenger_qty, trip_purpose))
            row = self.__cursor.lastrowid
        except sqlite3.Error as exc:
            self.close_connection()
            raise sqlite3.Error from exc
        else:
            self.__conn.commit()
            self.__trip_id = row

    def insert_telemetry(self, telemetry: dict) -> None:
        """
        Insert the telemetry data into the database. the telemetry must be in the appropriate format
        as the dictionary returned by ModbusQuery.read_and_format_telemetry_registers
        :param telemetry: the telemetry dictionary that returns the ModbusQuery class.
        :return: None
        """
        self.__timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.__cursor.execute('''
                INSERT INTO TelemetryData (telemetryTimeStamp,
                                            tripId,
                                            telemetryBatteryVoltageSystem,
                                            telemetryBatteryCurrentSystem,
                                            telemetryBatteryPowerSystem,
                                            telemetryBatteryStateOfChargeSystem,
                                            telemetryPVDCCoupledPower,
                                            telemetryPVDCCoupledCurrent,
                                            telemetryLatitude1,
                                            telemetryLatitude2,
                                            telemetryLongitude1,
                                            telemetryLongitude2,
                                            telemetryCourse,
                                            telemetrySpeed,
                                            telemetryGPSFix,
                                            telemetryGPSNumberOfSatellites,
                                            telemetryAltitude1,
                                            telemetryAltitude2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (self.__timestamp, self.__trip_id, telemetry["battery_voltage"],
                  telemetry["battery_current"], telemetry["battery_power"],
                  telemetry["battery_state_of_charge"], telemetry["pv-dc-coupled_power"],
                  telemetry["pv-dc-coupled_current"], telemetry["latitude1"],
                  telemetry["latitude2"], telemetry["longitude1"],
                  telemetry["longitude2"], telemetry["course"], telemetry["speed"],
                  telemetry["gps_fix"], telemetry["gps_number_of_satellites"],
                  telemetry["altitude1"], telemetry["altitude2"]))
        except sqlite3.Error as exe:
            self.close_connection()
            raise sqlite3.Error from exe
        else:
            self.__conn.commit()

    def end_of_trip(self) -> None:
        """
        Sets the trip_id attribute to None.
        :return: None
        """
        self.__trip_id = None

    def close_connection(self) -> int:
        """
        closes the connection.
        :return: 0
        """
        try:
            self.__conn.close()
        except sqlite3.Error as exe:
            pass
        else:
            return 0
