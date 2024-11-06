import time
import ttkbootstrap as ttk


class DataDisplayFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure((0,1,2), weight=1, uniform="a")

        self.left_pane: LeftPane = LeftPane(self)
        self.left_pane.grid(row=0, column=0, sticky="nsew")

        self.center_pane: CenterPane = CenterPane(self)
        self.center_pane.grid(row=0,column=1,sticky="nsew")

        self.right_pane: RightPane = RightPane(self)
        self.right_pane.grid(row=0,column=2,sticky="nsew")

        self.show_dock_mode()


    def show_dock_mode(self) -> None:
        self.center_pane.place_dock_mode_widgets()


    def show_trip_mode(self) -> None:
        self.center_pane.place_trip_mode_widgets()


class LeftPane(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)

        self.frame_configuration()

        # _________Widgets________
        self.date_and_time_variable: ttk.StringVar = ttk.StringVar()
        self.date_and_time_label: ttk.Label = ttk.Label(self,
                                       textvariable= self.date_and_time_variable, font=("Digital-7", 17))


        self.battery_soc_frame: ttk.Frame = self.title_widget_frame()
        self.title_battery_soc_percentage_level: ttk.Label = ttk.Label(self.battery_soc_frame,
                                                            text="Carga Batería (%)", font=("Digital-7", 17))
        self.battery_soc_percentage_flood_gauge = ttk.Floodgauge(self.battery_soc_frame,
                                                                 maximum=100,
                                                                 mask="Batería: {}%",
                                                                 orient="horizontal",
                                                                 bootstyle="success",
                                                                 value=0,
                                                                 font=("Digital-7", 17)
                                                                 )
        self.title_battery_soc_percentage_level.grid(column=0,row=0)
        self.battery_soc_percentage_flood_gauge.grid(column=0,row=1,
                                                     sticky="nsew", padx=10)
        self.battery_power_frame: ttk.Frame = self.title_widget_frame()
        self.title_battery_power_label :ttk.Label = ttk.Label(self.battery_power_frame,
                                                   text="Potencia Batería (w)", font=("Digital-7", 17))
        self.battery_power_variable: ttk.Variable = ttk.Variable(value="0")
        self.battery_power_label: ttk.Label = ttk.Label(self.battery_power_frame,
                                             textvariable=self.battery_power_variable,
                                             font=("Digital-7", 22)
                                             )
        self.title_battery_power_label.grid(column=0,row=0)
        self.battery_power_label.grid(column=0,row=1)


        self.place_widgets()
        self.show_date_and_time()


    def frame_configuration(self) ->None:
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure((1,2,3), weight=2, uniform="a")


    def title_widget_frame(self) ->ttk.Frame:
        frame: ttk.Frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.rowconfigure(0,weight=1, uniform="a")
        frame.rowconfigure(1, weight=3, uniform="a")
        return frame

    def place_widgets(self) ->None:
        self.date_and_time_label.grid(row=0, column=0, sticky="nsew", padx=10)
        self.battery_soc_frame.grid(row=1,column=0,sticky="nsew")
        self.battery_power_frame.grid(row=2,column=0,sticky="nesw")

    def show_date_and_time(self) ->None:
        current_date_time: str = time.strftime("%Y-%m-%d %H:%M:%S")
        self.date_and_time_variable.set(current_date_time)
        self.after(1000, self.show_date_and_time)


class CenterPane(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.frame_configuration()

        self.speed_frame = self.title_widget_frame()

        self.title_speed_label = ttk.Label(self.speed_frame,
                                           text="Velocidad", font=("Digital-7", 19))
        self.title_speed_label.grid(row=0,column=0)

        self.speed_indicator = ttk.Meter(self.speed_frame,
                                         metersize=250,
                                         amountused=4,
                                         metertype="semi",
                                         subtext="m/s",
                                         interactive=False,
                                         amounttotal=12,
                                         arcrange=180,
                                         arcoffset=180,
                                         bootstyle="info", textfont="-size 26 -weight bold", subtextfont="-size 14", subtextstyle="light")

        self.speed_indicator.grid(row=1,column=0,sticky="nsew")

        self.end_trip_button = ttk.Button(master=self,
                                          text="Terminar Viaje",
                                          style = "info.TButton")

        self.start_trip_button = ttk.Button(master=self,
                                            text="Iniciar Viaje",
                                            style = "info.TButton")


    def frame_configuration(self):
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=4, uniform="a")
        self.rowconfigure(2, weight=2, uniform="a")


    def title_widget_frame(self) -> ttk.Frame:
        frame: ttk.Frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.rowconfigure(0,weight=1, uniform="a")
        frame.rowconfigure(1, weight=3, uniform="a")
        return frame


    def place_dock_mode_widgets(self):
        self.speed_frame.grid_forget()
        self.end_trip_button.grid_forget()
        self.start_trip_button.grid(row=2, column=0, sticky="new")


    def place_trip_mode_widgets(self):
        self.start_trip_button.grid_forget()
        self.speed_frame.grid(row=1, column=0, sticky="nsew")
        self.end_trip_button.grid(row=2, column=0, sticky="new")


class RightPane(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.frame_configuration()

        self.load_power_frame = self.title_widget_frame()
        self.title_load_power_label = ttk.Label(self.load_power_frame,
                                                   text="Potencia Carga (w)", font=("Digital-7", 17))
        self.load_power_variable = ttk.Variable(value="0")
        self.load_power_label = ttk.Label(self.load_power_frame,
                                             textvariable=self.load_power_variable,
                                             font=("Digital-7", 20)
                                             )
        self.title_load_power_label.grid(column=0,row=0)
        self.load_power_label.grid(column=0,row=1)


        self.solar_power_frame = self.title_widget_frame()
        self.title_solar_power_label = ttk.Label(self.solar_power_frame,
                                                   text="Potencia Solar (w)", font=("Digital-7",17))
        self.solar_power_variable = ttk.Variable(value="0")
        self.solar_power_label = ttk.Label(self.solar_power_frame,
                                             textvariable=self.solar_power_variable,
                                             font=("Digital-7", 20)
                                             )
        self.title_solar_power_label.grid(column=0,row=0)
        self.solar_power_label.grid(column=0,row=1)

        self.place_widgets()


    def frame_configuration(self):
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure((1,2,3), weight=2, uniform="a")

    def title_widget_frame(self):
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.rowconfigure(0,weight=1, uniform="a")
        frame.rowconfigure(1, weight=3, uniform="a")
        return frame

    def place_widgets(self):
        self.load_power_frame.grid(row=1,column=0,sticky="nsew")
        self.solar_power_frame.grid(row=2,column=0,sticky="nesw")
