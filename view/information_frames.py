import ttkbootstrap as ttk

class InitiateTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window, passenger_number_var: ttk.IntVar):
        super().__init__(master)
        self.passenger_number_var = passenger_number_var
        self.columnconfigure((0,1), weight= 1, uniform="a")
        self.rowconfigure((0,1), weight=1, uniform="a")
        self.initiate_trip_text_var = ttk.StringVar()
        self.initiate_trip_label = ttk.Label(master=self,
                                             textvariable=self.initiate_trip_text_var, font=("Digital-7", 21))
        self.initiate_trip_label.grid(row=0, column=0, columnspan=2)
        self.yes_no_buttons()

    def yes_no_buttons(self):
        self.yes_button = ttk.Button(master=self,
                                   text= "Si",
                                   style="info.TButton")

        self.no_button = ttk.Button(master=self,
                                   text= "No",
                                   style="info.TButton")

        self.yes_button.grid(row=1,column=1, sticky="nw", padx=50)

        self.no_button.grid(row=1,column=0,sticky="ne", padx=50)

    def set_initiate_trip_text_var(self):
        string = f"Está seguro que quiere iniciar el viaje con {self.passenger_number_var.get()} pasajeros?"
        self.initiate_trip_text_var.set(string)

class FinishTripFrame(ttk.Frame):
    def __init__(self, master: ttk.Window):
        super().__init__(master)
        self.columnconfigure((0,1), weight= 1, uniform="a")
        self.rowconfigure((0,1), weight=1, uniform="a")
        self.end_trip_label = ttk.Label(master=self,
                                        text="Está seguro que quiere terminar el viaje?", font=("Digital-7", 22))
        self.end_trip_label.grid(row=0, column=0, columnspan=2)
        self.yes_no_buttons()

    def yes_no_buttons(self):
        self.yes_button = ttk.Button(master=self,
                                   text= "Si",
                                   style="info.TButton")

        self.no_button = ttk.Button(master=self,
                                   text= "No",
                                   style="info.TButton")

        self.yes_button.grid(row=1,column=1, sticky="nw", padx=50)

        self.no_button.grid(row=1,column=0,sticky="ne", padx=50)
