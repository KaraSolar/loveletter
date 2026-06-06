import queue
import threading


# La idea es:
# 1. Iniciar Viaje ve a

class ViewController:
    def __init__(self, view, data_base_queue: queue.Queue,
                 trip_start_signal_event: threading.Event):
        self.view = view
        self.data_base_queue = data_base_queue
        self.trip_start_signal_event = trip_start_signal_event
        self.configure_data_display_buttons()
        self.configure_initiate_trip_frame_buttons()
        self.configure_finish_trip_frame_buttons()
        self.configure_continue_buttons()
        self.configure_go_back_buttons()

    def configure_data_display_buttons(self):
        self.view.data_display_frame.center_pane.end_trip_button.config(
            command=lambda:self.view.raise_frame("finish_trip_frame"))
        self.view.data_display_frame.center_pane.start_trip_button.config(
            command=lambda:self.view.raise_frame("passenger_input_frame"))
        self.view.data_display_frame.right_pane.biodiversity_button.config(
            command=lambda:self.view.raise_frame("biodiversity_frame"))

    def configure_continue_buttons(self):
        self.view.passenger_input_frame.continue_button.config(
            command=lambda:self.view.raise_frame("captain_information_frame")
        )
        self.view.captain_information_frame.continue_button.config(
            command=lambda:self.view.raise_frame("trip_purposes_frame")
        )
        self.view.trip_purposes_frame.continue_button.config(
            command=lambda:self.view.raise_frame("multi_leg_trip_frame")
        )
        self.view.multi_leg_trip_frame.continue_button.config(
            command=lambda:self.view.raise_frame("departure_community_frame")
        )
        self.view.departure_community_frame.continue_button.config(
            command=lambda:self._navigate_to_departure_port()
        )
        self.view.departure_port_frame.continue_button.config(
            command=lambda:self.view.raise_frame("arrival_community_frame")
        )
        self.view.arrival_community_frame.continue_button.config(
            command=lambda:self._navigate_to_arrival_port()
        )
        self.view.arrival_port_frame.continue_button.config(
            command=lambda:self.change_initiate_trip_frame()
        )

    def configure_go_back_buttons(self):
        self.view.trip_purposes_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("captain_information_frame")
        )
        self.view.captain_information_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("passenger_input_frame")
        )
        self.view.passenger_input_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("data_display_frame")
        )
        self.view.multi_leg_trip_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("trip_purposes_frame")
        )
        self.view.departure_community_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("multi_leg_trip_frame")
        )
        self.view.departure_port_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("departure_community_frame")
        )
        self.view.arrival_community_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("departure_port_frame")
        )
        self.view.arrival_port_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("arrival_community_frame")
        )
        self.view.biodiversity_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("data_display_frame")
        )
        self.view.biodiversity_frame.register_button.config(
            command=lambda:self._navigate_to_biodiversity_input()
        )
        self.view.biodiversity_input_frame.go_back_button.config(
            command=lambda:self.view.raise_frame("biodiversity_frame")
        )
        self.view.biodiversity_input_frame.register_button.config(
            command=lambda:self.biodiversity_register()
        )

    def _navigate_to_biodiversity_input(self):
        self.view.biodiversity_input_frame.refresh()
        self.view.raise_frame("biodiversity_input_frame")

    def _navigate_to_departure_port(self):
        self.view.departure_port_frame.refresh()
        self.view.raise_frame("departure_port_frame")

    def _navigate_to_arrival_port(self):
        self.view.arrival_port_frame.refresh()
        self.view.raise_frame("arrival_port_frame")

    def change_initiate_trip_frame(self):
        self.view.initiate_trip_frame.set_initiate_trip_text_var()
        self.view.raise_frame("initiate_trip_frame")

    def configure_initiate_trip_frame_buttons(self):
        self.view.initiate_trip_frame.no_button.config(
            command=lambda:self.view.raise_frame("passenger_input_frame"))
        self.view.initiate_trip_frame.yes_button.config(
            command=self.initiate_trip_listener)

    def configure_finish_trip_frame_buttons(self):
        self.view.finish_trip_frame.no_button.config(
            command=lambda:self.view.raise_frame("data_display_frame"))
        self.view.finish_trip_frame.yes_button.config(
            command=self.end_trip_listener)

    def biodiversity_register(self):
        biodiversity = self.view.biodiversity_frame.biodiversity_var.get()
        sighting_count = self.view.biodiversity_input_frame.sighting_count_var.get()
        self.view.raise_frame("data_display_frame")
        self.data_base_queue.put({"type": "biodiversity",
                                  "value": {
                                      "biodiversity": biodiversity,
                                      "sighting_count": sighting_count}
                                  }
                                 )
        self.view.biodiversity_frame.refresh()
        self.view.biodiversity_input_frame.refresh()

    def initiate_trip_listener(self):
        trip_passenger_qty = self.view.passenger_input_frame.passenger_number_var.get()
        trip_purpose = self.view.trip_purposes_frame.trip_purpose_var.get()
        captain = self.view.captain_information_frame.captains_var.get()
        multi_leg_trip = self.view.multi_leg_trip_frame.multi_leg_trip_var.get()
        departure_community = self.view.departure_community_frame.community_var.get()
        departure_port = self.view.departure_port_frame.port_var.get()
        arrival_community = self.view.arrival_community_frame.community_var.get()
        arrival_port = self.view.arrival_port_frame.port_var.get()
        self.view.data_display_frame.show_trip_mode()
        self.view.raise_frame("data_display_frame")
        self.data_base_queue.put({"type":"trip",
                                  "value":{
                                      "passenger_number":trip_passenger_qty,
                                      "trip_purpose":trip_purpose,
                                      "captain":captain,
                                      "multi_leg_trip":multi_leg_trip,
                                      "departure_community":departure_community,
                                      "departure_port":departure_port,
                                      "arrival_community":arrival_community,
                                      "arrival_port":arrival_port}
                                  }
                                 )
        self.trip_start_signal_event.set()

    def end_trip_listener(self):
        self.view.data_display_frame.show_dock_mode()
        self.data_base_queue.put({"type":"end_trip"})
        self.trip_start_signal_event.clear()
        self.view.raise_frame("data_display_frame")
        self._refresh_trip_frames()

    def _refresh_trip_frames(self):
        self.view.passenger_input_frame.refresh()
        self.view.captain_information_frame.refresh()
        self.view.trip_purposes_frame.refresh()
        self.view.multi_leg_trip_frame.refresh()
        self.view.departure_community_frame.refresh()
        self.view.departure_port_frame.refresh()
        self.view.arrival_community_frame.refresh()
        self.view.arrival_port_frame.refresh()

    def update_view(self, telemetry: dict) -> None:
        # Update Course
        self.update_course(telemetry)
        # Update Battery State of Charge
        self.update_battery_soc(telemetry)
        # Update Solar Power
        self.update_solar_power(telemetry)
        # Update Load Power
        self.update_load_power(telemetry)
        # Update Speed
        self.update_speed(telemetry)

    def update_course(self, telemetry: dict) -> None:
        course = telemetry.get("course")
        if course:
            course = int(course / 100)
        self.view.data_display_frame.left_pane.course_indicator_variable.set(course)

    def update_battery_soc(self, telemetry: dict) -> None:
        battery_soc = telemetry.get("battery_state_of_charge")
        gauge_value = battery_soc if battery_soc is not None else -1
        self.view.data_display_frame.left_pane.battery_soc_percentage_flood_gauge.configure(value=gauge_value)

    def update_solar_power(self, telemetry: dict) -> None:
        solar_power = telemetry.get("pv-dc-coupled_power")
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
        speed_amount = round(speed_amount * 3.6, 2)  # Transform to km/h
        self.view.data_display_frame.center_pane.speed_indicator.configure(amountused=speed_amount)
