import queue
import threading
import ttkbootstrap
import time
from model.modbus_query import ModbusQuery
from model.telemetry_database import TelemetryDatabase


class WorkerModbus(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, queue_main_thread: queue.Queue,
                 stop_workers_signal: threading.Event, event_generate: ttkbootstrap.Window.event_generate,
                 trip_mode_flag_signal: threading.Event):
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.queue_main_thread = queue_main_thread
        self.stop_workers_signal = stop_workers_signal
        self.event_generate = event_generate
        self.modbus_query = ModbusQuery()
        self.trip_mode_flag_signal = trip_mode_flag_signal

    def set_telemetry_dict_to_none(self) -> None:
        """
        This function encapsulates replacing every value in the telemetry dict to None.
        :return: None
        """
        self.__telemetry = {key: None for key in self.__telemetry}

    for index, key in enumerate(self.__telemetry):
        self.__telemetry[key] = self.__register_values[index]

    def run(self):
        while not self.stop_workers_signal.is_set():
            telemetry: dict = self.modbus_query.read_and_format_telemetry_registers()
            self.queue_worker_database.put(["telemetry", telemetry])  # note that it passes a list
            self.queue_main_thread.put(telemetry)
            self.event_generate("<<update_view>>")
            if self.trip_mode_flag_signal.is_set():
                time.sleep(1)
            else:
                if self.trip_mode_flag_signal.wait(timeout=15):
                    continue
        self.modbus_query.disconnect()
        return 0


class WorkerDatabase(threading.Thread):
    def __init__(self, queue_worker_database: queue.Queue, stop_workers_signal: threading.Event):
        super().__init__(daemon=False)
        self.queue_worker_database = queue_worker_database
        self.stop_workers_signal = stop_workers_signal
        self.telemetry_database = TelemetryDatabase()

    def run(self):
        while not self.stop_workers_signal.is_set():
            message = self.queue_worker_database.get()
            if message[0] == "telemetry":
                self.telemetry_database.insert_telemetry(message[1])
            elif message[0] == "trip":
                self.telemetry_database.insert_trip(message[1])
            elif message[0] == "end_trip":
                self.telemetry_database.end_of_trip()
            else:
                raise ValueError("Not a valid queue message")
        self.telemetry_database.close_connection()
        return 0
