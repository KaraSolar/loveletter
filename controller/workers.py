"""
This module contains the modbus worker and the database worker
Both classes spawn a new thread, the modbus worker connects to
the modbus tcp and starts querying the sensors, listens for data
rate change signals and terminate signals. While the database
worker connects to the telemetry database, listens for signals
to write to the db and to terminate the thread.

NOTES:
We adhere to the recommendation of keeping a database connection in only one thread
and not passing it to other threads will remain open in second worker. There is a way to parse a conn object
to another thread by setting the check_same_thread = False in sqlite3, however, that will complicate
more the software will little to no gain. This also applies for modbus tcp connection,
it will remain open in first worker and not be passed anywhere else (this module pymodbus is not
thread safe).

Note Daemon threads are abruptly stopped at shutdown. Their resources (such as open files,
database transactions, etc.) may not be released properly. If you want your threads to stop gracefully,
make them non-daemonic and use a suitable signalling mechanism such as an Event.

TO DO:
Logs for unexpected exceptions.
"""

import queue
import threading
import ttkbootstrap as ttk
import time
import copy
from model.modbus_query import ModbusQuery
from model.telemetry_database import TelemetryDatabase
from model.canbus_query import CanBusQuery
from model.gps_query import GPSQuery


class WorkerModbus(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, stop_workers_signal: threading.Event,
                 event_generate: ttk.Window.event_generate, trip_mode_flag_signal: threading.Event,
                 queue_view: queue.Queue, server_ip_config: str):
        """Initialize a new thread instance, does not run automatically.
        This new thread will query the modbus every second or 15 seconds depending on signals,
        put the telemetry data in two queues and listen for command signals.
        Args:
            queue_worker_database (queue.Queue, required): a queue object used to send telemetry data across threads.
            stop_workers_signal (threading.Event, required): an event, when set the thread will terminate.
            event_generate (ttkbootstrap.Window.event_generate, required): a ttkbootstrap method used to notify the main thread to update the view.
            trip_mode_flag_signal (threading.Event, required): an event, when set the sampling rate will change.
            queue_view (queue.Queue, required): a queue object used to send telemetry data across threads.
        """
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.stop_workers_signal = stop_workers_signal
        self.event_generate = event_generate
        self.trip_mode_flag_signal = trip_mode_flag_signal
        self.queue_view = queue_view
        self.server_ip_config = server_ip_config

    def run(self) -> int:
        """Start the querying loop in the WorkerModbus thread.

        This method continuously queries the Modbus, formats telemetry data,
        and sends it to the appropriate queues. It also updates the view when required.

        :return: 0 when terminated.
        """
        modbus_query = ModbusQuery(server_ip=self.server_ip_config)  # Initialize in the new thread to avoid race conditions.
        while not self.stop_workers_signal.is_set():
            telemetry_modbus: dict = modbus_query.read_and_format_telemetry_registers()
            self.queue_worker_database.put({"type": "telemetry", "value": telemetry_modbus})
            self.queue_view.put(telemetry_modbus)
            if not self.stop_workers_signal.is_set():
                self.event_generate("<<update_view>>")  # Blocking event tkinter events are not thread safe.
            if self.trip_mode_flag_signal.is_set():
                time.sleep(1)
            else:
                if self.trip_mode_flag_signal.wait(timeout=15):
                    continue
        modbus_query.disconnect()
        return 0


class WorkerDatabase(threading.Thread):
    """Initialize a new thread instance, does not run automatically.
    This new thread will wait for a queue message and call the appropriate insert methods or
    terminate the thread.
    Args:
        queue_worker_database (queue.Queue, required): a queue object used to send telemetry data across threads.
    """
    def __init__(self, queue_worker_database: queue.Queue,
                 db_name: str, passenger_number_config: dict, trip_purposes_config: list):
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.db_name = db_name
        self.passenger_number_config = passenger_number_config
        self.trip_purposes_config = trip_purposes_config

    def run(self):
        """Start the queue listening.

        This method continuously listens for the worker_database queue,
        call the appropriate insert methods or terminate the thread.

        :return: 0 when terminated.
        """
        telemetry_database = TelemetryDatabase(self.db_name,
                                               passenger_number_config=self.passenger_number_config,
                                               trip_purposes_config=self.trip_purposes_config)  # Initialize within the new thread otherwise race conditions.
        while True:
            message = self.queue_worker_database.get()
            message_type = message["type"]
            if message_type == "telemetry":
                telemetry_database.insert_telemetry(message["value"])
            elif message_type == "trip":
                telemetry_database.insert_trip(value=message["value"])
            elif message_type == "end_trip":
                telemetry_database.end_of_trip()
            elif message_type == "destroy":
                break
            else:
                telemetry_database.close_connection()
                raise ValueError("Not a valid type.")
        telemetry_database.close_connection()
        return 0


class WorkerCanBusGps(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, stop_workers_signal: threading.Event,
                 event_generate: ttk.Window.event_generate, trip_mode_flag_signal: threading.Event,
                 queue_view: queue.Queue, channel_config: str):

        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.stop_workers_signal = stop_workers_signal
        self.event_generate = event_generate
        self.trip_mode_flag_signal = trip_mode_flag_signal
        self.queue_view = queue_view
        self.channel_config = channel_config
        self.__telemetry: dict = {"battery_voltage": None, "battery_current": None,
                                  "battery_power": None, "battery_state_of_charge": None,
                                  "pv-dc-coupled_power": None, "pv-dc-coupled_current": None,
                                  "latitude1": None, "latitude2": None, "longitude1": None,
                                  "longitude2": None, "course": None, "speed": None,
                                  "gps_fix": None, "gps_number_of_satellites": None,
                                  "altitude1": None, "altitude2": None}

    def run(self) -> int:
        """Start the querying loop in the WorkerModbus thread.

        This method continuously queries the Modbus, formats telemetry data,
        and sends it to the appropriate queues. It also updates the view when required.

        :return: 0 when terminated.
        """
        canbus_query = CanBusQuery(
            channel=self.channel_config)  # Initialize in the new thread to avoid race conditions.
        gps_query = GPSQuery()
        while not self.stop_workers_signal.is_set():
            battery_telemetry: dict = canbus_query.read_and_format_can_bus_message()
            # Battery Telemetry (CanBus)
            self.__telemetry["battery_voltage"] = battery_telemetry["voltage"]
            self.__telemetry["battery_current"] = battery_telemetry["current"]
            self.__telemetry["battery_state_of_charge"] = battery_telemetry["soc"]
            self.__telemetry["battery_power"] = battery_telemetry["battery_power"]
            # GPS Telemetry (GPS)
            gps_telemetry: dict = gps_query.read_and_format_gps_signal()
            self.__telemetry["latitude1"] = gps_telemetry["latitude"]
            self.__telemetry["longitude1"] = gps_telemetry["longitude"]
            self.__telemetry["course"] = gps_telemetry["course"]
            self.__telemetry["speed"] = gps_telemetry["speed"]
            self.__telemetry["gps_fix"] = gps_telemetry["gps_fix"]
            self.__telemetry["gps_number_of_satellites"] = gps_telemetry["gps_number_of_satellites"]
            self.__telemetry["altitude1"] = gps_telemetry["altitude"]
            # Put in the queue
            telemetry_modbus_copy = copy.deepcopy(self.__telemetry)
            self.queue_worker_database.put({"type": "telemetry", "value": telemetry_modbus_copy})
            self.queue_view.put(telemetry_modbus_copy)
            if not self.stop_workers_signal.is_set():
                self.event_generate("<<update_view>>")  # Blocking event tkinter events are not thread safe.
            if self.trip_mode_flag_signal.is_set():
                time.sleep(1)
            else:
                if self.trip_mode_flag_signal.wait(timeout=15):
                    continue
        canbus_query.disconnect()
        gps_query.disconnect()
        return 0
