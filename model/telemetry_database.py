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
import logging


logging.basicConfig(level=logging.DEBUG, filename=f"loggings/telemetry_database.log",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")


class TelemetryDatabase:
    """
    As per sqlite3 api documentation: Note The context manager neither implicitly opens a new
    transaction nor closes the connection.
    """
    def __init__(self, db_name: str = "model/telemetry.db"):
        """
        Instantiate the connection to the database and create the tables.
        :param db_name: str expects a string constraint to "model/telemetry.db",
        "model/dev_telemetry.db", "model/test_telemetry.db" won't admit other values
        """
        self.db_name = db_name
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
        allowed_strings = ["model/telemetry.db", "model/dev_telemetry.db", "model/test_telemetry.db"]
        if db_name not in allowed_strings:
            logging.exception("not valid database.")
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
            logging.exception("Couldn't connect to database.")
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
                                tripPassengerQty INTEGER NOT NULL
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
            logging.exception("Couldn't connect to database.")
            self.close_connection()
            raise sqlite3.Error from exc
        else:
            self.__conn.commit()

    def insert_trip(self, trip_passenger_qty: int) -> None:
        """
        Inserts a new trip row to the Trip table with the number of passengers given.
        When successful assigns the attribute trip_id to the trip id.
        :param trip_passenger_qty: int greater than 0 but lower than 20, required
        :return: None
        :raises: ValueError if passenger None, less than 0 or higher than 20.
        :raises: sqlite3.Error if database error.
        """
        if trip_passenger_qty is None:
            logging.exception(f"trip passenger NULL")
            raise ValueError("passenger can't be NULL")
        if not isinstance(trip_passenger_qty, int):
            raise ValueError("passenger must be int.")
        if trip_passenger_qty > 20 or trip_passenger_qty < 0:
            logging.exception(f"trip passenger incorrect: {trip_passenger_qty}")
            raise ValueError("passengers not in range")
        try:
            self.__cursor.execute('''
                INSERT INTO Trip(tripPassengerQty) VALUES(?)
            ''', (trip_passenger_qty,))
            row = self.__cursor.lastrowid
        except sqlite3.Error as exc:
            logging.exception(f"trip passenger incorrect: {trip_passenger_qty}")
            self.close_connection()
            raise sqlite3.Error from exc
        else:
            self.__conn.commit()
            self.__trip_id = row

    def insert_telemetry(self, telemetry: dict) -> None:
        """
        Insert the telemetry data into the database. the telemetry must be in the appropiate format
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
            logging.exception(f"telemetry not in the appropiate format: {telemetry}")
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
            logging.exception("error during closure")
        else:
            return 0