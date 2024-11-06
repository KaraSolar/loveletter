'''
This module contains the class PassengerInput, part of the VIEW.
'''

import ttkbootstrap as ttk

class PassengerInput(ttk.Frame):
    '''
    A class to represent the Frame Passenger Input, in this frame the user
    can insert the number of passengers, go back to dock mode, or initialize
    the trip. Inherints from ttk.Frame
    ...

    Attributes
    ----------
    master : ttk.Window
        master (Window) of a ttk.Frame
    label_font_size : tuple
        font size of label that will be displayed.

    Methods
    -------
    passenger_number_label_and_buttons() ->None:
        create and place the passenger label and button objects in the GUI.
    
    action_buttons() -> None:
        create and place the action buttons (initiate trip and go back) objects
        in the GUI.
    
    decrease_passenger_number() ->None:
        decrease the variable passenger_number_var by 1.

    increase_passenger_number() ->None:
        increase the variable passenger_number_var by 1.

    show_message_box_initiate_trip() -> Messagebox:
        returns a Messagebox object to prompt the user to initiate the trip
        with the selected number of passengers.    
    '''

    def __init__(self, master: ttk.Window, label_font_size:tuple, passenger_number_config):
        super().__init__(master)

        # ____________Initialize Variables __________
        self.passenger_number_config = passenger_number_config
        self.max_passenger: int = self.passenger_number_config["max"]
        self.min_passenger: int = self.passenger_number_config["min"]
        self.label_font_size: tuple = label_font_size
        self.passenger_number_var: ttk.IntVar = ttk.IntVar(value=self.min_passenger)

        # ____________FrameConfiguration_____________
        self.columnconfigure((0,1,2), weight= 1, uniform="a")

        self.rowconfigure((0,1,2), weight=1, uniform="a")

        self.passenger_number_label_and_buttons()
        self.action_buttons()

    # _________________Methods_____________________________


    def passenger_number_label_and_buttons(self) ->None:
        
        # _____________Passenger Number Buttons____________

        self.decrease_passenger_button:ttk.Button = ttk.Button(master=self,
                                       text= "Menos",
                                       style="info.TButton",
                                       command=self.decrease_passenger_number)
        self.decrease_passenger_button.grid(row=1, column=0, sticky="ens")

        self.increase_passenger_button:ttk.Button = ttk.Button(master=self,
                                                    style="info.TButton",
                                                    text= "Mas",
                                                    width=6,
                                                    command=self.increase_passenger_number)
        self.increase_passenger_button.grid(row=1, column=2, sticky="wns")


        # _______________Passenger Indicator______________
        self.passenger_number_label:ttk.Label = ttk.Label(master=self,
                                          textvariable = self.passenger_number_var,
                                          font=("Digital-7", 40))
        self.passenger_number_label.grid(row=1, column=1, sticky="ns")


    def action_buttons(self) -> None:
        # _______________Start Trip________________________
        self.start_trip_button:ttk.Button = ttk.Button(master=self,
                                            text="Iniciar Viaje",
                                            style="info.TButton")
        self.start_trip_button.grid(row=2, column=1, sticky="ew")


        # _______________Go back _________________________
        self.go_back_button:ttk.Button = ttk.Button(self,
                                         text="Regresar",
                                         style="info.TButton")
        self.go_back_button.grid(row=0, column=1, sticky="ew")


    # ________________command methods_____________________
    def decrease_passenger_number(self) ->None:
        n:int = self.passenger_number_var.get()
        if n > self.min_passenger:
            self.passenger_number_var.set(n-1)


    def increase_passenger_number(self) ->None:
        n:int = self.passenger_number_var.get()
        if n < self.max_passenger:
            self.passenger_number_var.set(n+1)
