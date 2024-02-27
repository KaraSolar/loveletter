from controller.main import Controller
from view.main import View

if __name__ == "__main__":
    try:
        view = View()
        controller = Controller(view)
        view.start_mainloop()
    except KeyboardInterrupt:
        controller.close_on_escape()
