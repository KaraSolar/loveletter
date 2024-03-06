from controller.main import Controller
from view.main import View
import logging

if __name__ == "__main__":
    # TODO: create the logging hierarchy and pass it to the modules.
    try:
        view = View()
        controller = Controller(view)
        view.start_mainloop()
    except KeyboardInterrupt:
        controller.close_on_escape()
