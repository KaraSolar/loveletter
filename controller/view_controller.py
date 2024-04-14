import queue
import threading


class ViewController:
    def __init__(self, view, data_base_queue: queue.Queue,
                 trip_start_signal_event: threading.Event):
        self.view = view
        self.data_base_queue = data_base_queue
        self.trip_start_signal_event = trip_start_signal_event
        self.configure_data_display_buttons()
        self.configure_passenger_input_buttons()
        self.configure_initiate_trip_frame_buttons()
        self.configure_finish_trip_frame_buttons()

    def configure_data_display_buttons(self):
        self.view.data_display_frame.center_pane.end_trip_button.config(
            command=lambda: self.view.raise_frame("finish_trip_frame"))
        self.view.data_display_frame.center_pane.start_trip_button.config(
            command=lambda: self.view.raise_frame("passenger_input_frame"))

    def configure_passenger_input_buttons(self):
        self.view.passenger_input_frame.start_trip_button.config(
            command=self.change_initiate_trip_frame)
        self.view.passenger_input_frame.go_back_button.config(
            command=lambda: self.view.raise_frame("data_display_frame"))

    def change_initiate_trip_frame(self):
        self.view.initiate_trip_frame.set_initiate_trip_text_var()
        self.view.raise_frame("initiate_trip_frame")

    def configure_initiate_trip_frame_buttons(self):
        self.view.initiate_trip_frame.no_button.config(
            command=lambda: self.view.raise_frame("passenger_input_frame"))
        self.view.initiate_trip_frame.yes_button.config(
            command=self.initiate_trip_listener)

    def configure_finish_trip_frame_buttons(self):
        self.view.finish_trip_frame.no_button.config(
            command=lambda: self.view.raise_frame("data_display_frame"))
        self.view.finish_trip_frame.yes_button.config(
            command=self.end_trip_listener)

    def initiate_trip_listener(self):
        passenger_number = self.view.passenger_input_frame.passenger_number_var.get()
        self.view.data_display_frame.show_trip_mode()
        self.view.raise_frame("data_display_frame")
        self.data_base_queue.put({"type": "trip", "value": passenger_number})
        self.trip_start_signal_event.set()

    def end_trip_listener(self):
        self.view.data_display_frame.show_dock_mode()
        self.data_base_queue.put({"type": "end_trip"})
        self.trip_start_signal_event.clear()
        self.view.raise_frame("data_display_frame")

    def update_view(self, telemetry: dict) -> None:
        # Update Battery Power
        self.update_battery_power(telemetry)
        # Update Battery State of Charge
        self.update_battery_soc(telemetry)
        # Update Solar Power
        self.update_solar_power(telemetry)
        # Update Load Power
        self.update_load_power(telemetry)
        # Update Speed
        self.update_speed(telemetry)

    def update_battery_power(self, telemetry: dict) -> None:
        battery_power = telemetry.get("battery_power")
        if battery_power is not None:
            self.view.data_display_frame.left_pane.battery_power_variable.set(battery_power)

    def update_battery_soc(self, telemetry: dict) -> None:
        battery_soc = telemetry.get("battery_state_of_charge")
        gauge_value = battery_soc if battery_soc is not None else -1
        self.view.data_display_frame.left_pane.battery_soc_percentage_flood_gauge.configure(value=gauge_value)

    def update_solar_power(self, telemetry: dict) -> None:
        solar_power = telemetry.get("pv-dc-coupled_power")
        if solar_power is not None:
            self.view.data_display_frame.right_pane.solar_power_variable.set(solar_power)

    def update_load_power(self, telemetry: dict) -> None:
        battery_power = telemetry.get("battery_power")
        solar_power = telemetry.get("pv-dc-coupled_power")
        if battery_power is not None and solar_power is not None:
            load_power = battery_power - solar_power
            self.view.data_display_frame.right_pane.load_power_variable.set(load_power)
        else:
            self.view.data_display_frame.right_pane.load_power_variable.set(None)

    def update_speed(self, telemetry: dict) -> None:
        speed = telemetry.get("speed")
        speed_amount = speed if speed is not None else 0
        self.view.data_display_frame.center_pane.speed_indicator.configure(amountused=speed_amount)
