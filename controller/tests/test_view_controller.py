import time

import pytest
from controller.view_controller import ViewController
import threading
import queue
from view.main import View


@pytest.fixture(scope="function", autouse=True)
def view_controller() -> ViewController:
    view = View()
    view.passenger_input_frame.passenger_number_var.set(20)
    data_base_queue = queue.Queue()
    trip_start_signal_event = threading.Event()
    view_controller = ViewController(view=view,
                                     data_base_queue=data_base_queue,
                                     trip_start_signal_event=trip_start_signal_event)
    yield trip_start_signal_event, data_base_queue, view_controller
    view.root.destroy()

def test_initiate_trip_listener(view_controller):
    trip_start_signal_event, data_base_queue, view_controller = view_controller
    view_controller.initiate_trip_listener()
    assert trip_start_signal_event.is_set()
    message = data_base_queue.get()
    type = message["type"]
    value = message["value"]
    assert type == "trip"
    assert value == 20


