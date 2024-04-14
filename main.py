from controller.main import Controller
from view.main import View
import logging


logging.basicConfig(level=logging.DEBUG, filename=f"loggings/modbus_query.log",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    # TODO: create the logging hierarchy and pass it to the modules.
    view = View()
    controller = Controller(view=view, db_name="model/telemetry.db")
    try:
        view.start_mainloop()
    except KeyboardInterrupt:
        controller.close_on_escape()
