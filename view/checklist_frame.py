import time
import ttkbootstrap as ttk


class ChecklistFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)
        self.rowconfigure(0, weight=2)
        self.rowconfigure((1,2,3,4,5,6,7,8), weight=1, uniform="a")
        self.rowconfigure(9, weight=2)
        self.columnconfigure(0, weight=1, uniform="a")

        # _______________ Go back Button ___________________
        self.go_back_frame = ttk.Frame(self)
        self.go_back_frame.columnconfigure((0,1,2), weight=1, uniform="a")
        self.go_back_frame.rowconfigure(0, weight=1, uniform="a")
        self.go_back_frame.grid(row=0, column=0, sticky="nsew")
        self.go_back_button:ttk.Button = ttk.Button(master=self.go_back_frame,
                                         text="Regresar",
                                         style="info.TButton")
        self.go_back_button.grid(row=0, column=1, sticky="sew")

        # ______________ Initiate Trip Button _______________
        self.initiate_trip_frame = ttk.Frame(self)
        self.initiate_trip_frame.columnconfigure((0,1,2), weight=1, uniform="a")
        self.initiate_trip_frame.rowconfigure(0, weight=1, uniform="a")
        self.initiate_trip_frame.grid(row=9, column=0, sticky="nsew")
        self.initiate_trip_button:ttk.Button = ttk.Button(master=self.initiate_trip_frame,
                                         text="Iniciar Viaje",
                                         style="info.TButton")
        self.initiate_trip_button.grid(row=0, column=1, sticky="new")


        # ______________ Checkboxes __________________________
        self.first_check = ttk.Checkbutton(self, text='Asegúrate de que las baterías estén completamente cargadas', style = "success.TCheckbutton")
        self.second_check = ttk.Checkbutton(self, text='Asegúrate de tener suficientes salvavidas para todos los pasajeros', style = "success.TCheckbutton")
        self.third_check = ttk.Checkbutton(self, text='Asegúrate de que esté completamente surtido el botiquin y en un lugar accesible', style="success.TCheckbutton")
        self.first_check.grid(row=1, column=0, sticky='nsew', padx=40)
        self.second_check.grid(row=2, column=0, sticky='nsew', padx=40)
        self.third_check.grid(row=3, column=0, sticky='nsew', padx=40)

        print(self.first_check.state())
        self.first_check.invoke()
        print(self.first_check.state())
        self.first_check.invoke()
        print(self.first_check.state())

    # https://stackoverflow.com/questions/4236910/getting-checkbutton-state
