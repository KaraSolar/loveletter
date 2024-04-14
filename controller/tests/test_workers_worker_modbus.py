import pytest
import threading
import queue
from controller.workers import WorkerModbus
from modbus_simulator.simulator_for_test import run_server
import multiprocessing
import time
import ttkbootstrap as ttk


@pytest.fixture(scope="function", autouse=True)
def start_server() -> multiprocessing.Process:
    start_server = multiprocessing.Process(target=run_server)
    start_server.start()
    time.sleep(2)
    yield start_server
    start_server.terminate()  # clean up after tests are done


@pytest.fixture(scope="function", autouse=True)
def worker_modbus() -> WorkerModbus:
    queue_worker_database = queue.Queue()
    stop_workers_signal = threading.Event()
    window = ttk.Window()
    trip_mode_flag_signal = threading.Event()
    queue_view = queue.Queue()
    worker_modbus = WorkerModbus(queue_worker_database=queue_worker_database,
                                 stop_workers_signal=stop_workers_signal,
                                 event_generate=window.event_generate,
                                 trip_mode_flag_signal=trip_mode_flag_signal,
                                 queue_view=queue_view)
    yield (queue_worker_database, stop_workers_signal, window, trip_mode_flag_signal,
           queue_view, worker_modbus)  # yields the set-up of the thread every function must start it.
    # Terminate the thread.
    stop_workers_signal.set()
    worker_modbus.join()  # blocks main until worker terminated.
    while True:
        if worker_modbus.is_alive():
            time.sleep(1)
        return 0


def test_database_queue(start_server, worker_modbus):
    queue_worker_database, stop_workers_signal, window, trip_mode_flag_signal, queue_view, worker_modbus_instance = worker_modbus
    worker_modbus_instance.start()
    time.sleep(3)
    message_database = queue_worker_database.get()  # First telemetry reading is 0.
    assert message_database["type"] == "telemetry"
    assert message_database["value"]["battery_voltage"] == 0


def test_virtual_event_and_view_queue(start_server, worker_modbus):
    queue_worker_database, stop_workers_signal, window, trip_mode_flag_signal, queue_view, worker_modbus_instance = worker_modbus
    worker_modbus_instance.start()
    time.sleep(3)
    message_view = queue_view.get()  # First telemetry reading is 0.
    assert message_view["battery_voltage"] == 0
    event_info = window.event_info("<<update_view>>")
    assert event_info is not None


def test_stop_thread(start_server, worker_modbus):
    queue_worker_database, stop_workers_signal, window, trip_mode_flag_signal, queue_view, worker_modbus_instance = worker_modbus
    worker_modbus_instance.start()
    time.sleep(3)
    stop_workers_signal.set()
    time.sleep(2)
    assert not worker_modbus_instance.is_alive()
