from .root import Root
from .passenger_input_frame import PassengerInput
from .data_display_frame import DataDisplayFrame
from .information_frames import InitiateTripFrame,FinishTripFrame


class View():

    def __init__(self):
        self.root = Root()
        self.root.rowconfigure(0,weight=1,uniform="a")
        self.root.columnconfigure(0,weight=1,uniform="a")

        self.frames = {}
        self.passenger_input_frame = PassengerInput(self.root, self.root.indicator_font)
        self.initiate_trip_frame = InitiateTripFrame(self.root, self.passenger_input_frame.passenger_number_var)
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
