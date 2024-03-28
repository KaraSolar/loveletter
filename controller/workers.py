"""
TO DO:

Consider changing the telemetry_data_bus to a @dataclass.
"""

import queue
import threading
import ttkbootstrap
import time
from model.modbus_query import ModbusQuery
from model.telemetry_database import TelemetryDatabase


class WorkerModbus(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, stop_workers_signal: threading.Event,
                 event_generate: ttkbootstrap.Window.event_generate, trip_mode_flag_signal: threading.Event,
                 lock: threading.Lock, telemetry_data_bus: dict):
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.stop_workers_signal = stop_workers_signal
        self.event_generate = event_generate
        self.modbus_query = ModbusQuery()
        self.trip_mode_flag_signal = trip_mode_flag_signal
        self.lock = lock
        self.telemetry_data_bus = telemetry_data_bus

    def write_telemetry_data_bus(self, telemetry_modbus):
        with self.lock:
            for index, key in enumerate(self.telemetry_data_bus):
                self.telemetry_data_bus[key] = telemetry_modbus[index]

    def run(self):
        while not self.stop_workers_signal.is_set():
            telemetry_modbus: list = self.modbus_query.read_and_format_telemetry_registers()
            self.write_telemetry_data_bus(telemetry_modbus=telemetry_modbus)
            self.queue_worker_database.put("telemetry")
            self.event_generate("<<update_view>>")
            if self.trip_mode_flag_signal.is_set():
                time.sleep(1)
            else:
                if self.trip_mode_flag_signal.wait(timeout=15):
                    continue
        self.modbus_query.disconnect()
        return 0


class WorkerDatabase(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, telemetry_data_bus: dict, lock: threading.Lock):
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.telemetry_data_bus = telemetry_data_bus
        self.lock = lock
        self.telemetry_database = TelemetryDatabase()

    def run(self):
        while True:
            message = self.queue_worker_database.get()
            if message == "telemetry":
                with self.lock:
                    self.telemetry_database.insert_telemetry(self.telemetry_data_bus)
            elif message == "end_trip":
                self.telemetry_database.end_of_trip()
            elif message == "destroy":
                break
            else:
                self.telemetry_database.insert_trip(message)
        self.telemetry_database.close_connection()
        return 0
