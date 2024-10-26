from .root import Root
from .passenger_input_frame import PassengerInput
from .data_display_frame import DataDisplayFrame
from .information_frames import InitiateTripFrame,FinishTripFrame, TripPurposeWarning


class View():
    def __init__(self, passenger_number_config, trip_purposes_config: list):
        self.passenger_number_config = passenger_number_config
        self.trip_purposes_config = trip_purposes_config
        self.root = Root()
        self.root.rowconfigure(0,weight=1,uniform="a")
        self.root.columnconfigure(0,weight=1,uniform="a")

        self.frames = {}
        self.passenger_input_frame = PassengerInput(self.root, self.root.indicator_font,
                                                    self.passenger_number_config,
                                                    trip_purposes_config=self.trip_purposes_config)
        self.initiate_trip_frame = InitiateTripFrame(self.root, self.passenger_input_frame.passenger_number_var,
                                                     self.passenger_input_frame.trip_purpose_var)
        self.trip_purpose_warning = TripPurposeWarning(self.root,
                                                       trip_purposes_var=self.passenger_input_frame.trip_purpose_var)
        self.trip_purpose_warning.close_warning_button.config(command=self.trip_purpose_warning.grid_forget)
        self.finish_trip_frame = FinishTripFrame(self.root)
        self.data_display_frame = DataDisplayFrame(self.root)
        self.frames["passenger_input_frame"] = self.passenger_input_frame
        self.frames["data_display_frame"] = self.data_display_frame
        self.frames["initiate_trip_frame"] = self.initiate_trip_frame
        self.frames["finish_trip_frame"] = self.finish_trip_frame

        for value in self.frames.values():
            value.grid(row=0,column=0,sticky="nesw")
        self.raise_frame("data_display_frame")


    def raise_frame(self, frame):
        self.frames[frame].lift()

    def start_mainloop(self):
        self.root.mainloop()

    def trip_purpose_validator(self):
        if self.passenger_input_frame.trip_purpose_var.get() in self.trip_purposes_config:
            return True
        else:
            self.trip_purpose_warning.set_warning_text_var()
            self.trip_purpose_warning.grid(row=0, column=0, sticky="nsew")
            self.trip_purpose_warning.lift()
