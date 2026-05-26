from .root import Root
from .data_display_frame import DataDisplayFrame
from .information_frames import InitiateTripFrame, FinishTripFrame, TripPurposeWarning
from .captain_information_frame import CaptainInformation
from .passenger_input_frame import PassengerInput
from .trip_purposes_frame import TripPurposes
from .multi_leg_trip_frame import MultiLegTrip


class View():
    def __init__(self, passenger_number_config, trip_purposes_config: list, list_captain_config: list):
        self.passenger_number_config = passenger_number_config
        self.trip_purposes_config = trip_purposes_config
        self.captain_config = list_captain_config
        self.root = Root()
        self.root.rowconfigure(0, weight=1, uniform="a")
        self.root.columnconfigure(0, weight=1, uniform="a")

        self.frames = {}
        self.captain_information_frame = CaptainInformation(self.root, self.root.indicator_font,
                                                            self.captain_config)
        self.passenger_input_frame = PassengerInput(self.root, self.root.indicator_font,
                                                    self.passenger_number_config)
        self.trip_purposes_frame = TripPurposes(self.root, self.root.indicator_font, self.trip_purposes_config)
        self.trip_purpose_warning_frame = TripPurposeWarning(self.root,
                                                             trip_purposes_var=self.trip_purposes_frame.trip_purpose_var)
        self.trip_purpose_warning_frame.close_warning_button.config(
            command=lambda:self.close_trip_purpose_warning_frame())
        self.finish_trip_frame = FinishTripFrame(self.root)
        self.data_display_frame = DataDisplayFrame(self.root)
        self.multi_leg_trip_frame = MultiLegTrip(self.root, self.root.indicator_font)
        self.initiate_trip_frame = InitiateTripFrame(self.root, self.passenger_input_frame.passenger_number_var,
                                                     self.trip_purposes_frame.trip_purpose_var,
                                                     self.captain_information_frame.captains_var,
                                                     self.multi_leg_trip_frame.multi_leg_trip_var)
        self.frames["data_display_frame"] = self.data_display_frame
        self.frames["finish_trip_frame"] = self.finish_trip_frame
        self.frames["trip_purpose_warning"] = self.trip_purpose_warning_frame
        self.frames["captain_information_frame"] = self.captain_information_frame
        self.frames["passenger_input_frame"] = self.passenger_input_frame
        self.frames["trip_purposes_frame"] = self.trip_purposes_frame
        self.frames["initiate_trip_frame"] = self.initiate_trip_frame
        self.frames["multi_leg_trip_frame"] = self.multi_leg_trip_frame

        for value in self.frames.values():
            value.grid(row=0, column=0, sticky="nsew")
        self.raise_frame("data_display_frame")

    def raise_frame(self, frame):
        if self.trip_input_validator(frame):
            self.frames[frame].lift()

    def start_mainloop(self):
        self.root.mainloop()

    def trip_input_validator(self, validation_frame: str) -> bool:
        # doesn't make sense anymore, needs to be generic
        # needs to be called b4 any frame continue.
        '''Validates if the selected trip purpose is in the configured list.
        :return: bool: True if purpose is valid, False otherwise
        '''
        if validation_frame == "multi_leg_trip_frame":
            if self.trip_purposes_frame.trip_purpose_var.get() in self.trip_purposes_config:
                return True
            print("wrong trip purpose")
            self.trip_purpose_warning_frame.set_warning_text_var(validation_frame)
            self.raise_frame(frame="trip_purpose_warning")
        elif validation_frame == "trip_purposes_frame":
            if self.captain_information_frame.captains_var.get() in self.captain_config:
                return True
            print("wrong captain info")
            self.trip_purpose_warning_frame.set_warning_text_var(validation_frame)
            self.raise_frame(frame="trip_purpose_warning")
        else:
            return True

    def close_trip_purpose_warning_frame(self):
        if not self.captain_information_frame.captains_var.get():
            self.raise_frame(frame="captain_information_frame")
        elif not self.trip_purposes_frame.trip_purpose_var.get():
            self.raise_frame(frame="trip_purposes_frame")
        else:
            self.raise_frame(frame="passenger_input_frame")
