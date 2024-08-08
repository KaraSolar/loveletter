import ttkbootstrap as ttk

class Root(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg",
                         title="Love Letter")
        self.geometry("800x412+0+0")
        self.resizable(False,False)
        self.update_idletasks()
        # Title fonts
        # Indicator (Label Fonts)
        # Clock Font (could also work for battery gauge for example)
        self.title_font: tuple = ("Digital-7", 20)
        self.indicator_font: tuple = ("Digital-7", 18)
        style = ttk.Style()
        style.configure('info.TButton', font=self.title_font)

    def get_screen_resolution(self) -> tuple:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        return screen_width, screen_height
