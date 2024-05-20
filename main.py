from controller.main import Controller
from view.main import View
import logging
from config.config_reader import read_config

config = read_config()
db_name_config = config["database"]["name"]
server_ip_config = config["cerbo_gx"]["server_ip"]
passenger_number_config: dict = config["passenger_number"]
logging.basicConfig(level=logging.ERROR, filename=f"loggings/telemetry_database.log",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    # TODO: create the logging hierarchy and pass it to the modules.
    view = View(passenger_number_config)
    controller = Controller(view=view, db_name=f"model/{db_name_config}",
                            server_ip_config=server_ip_config,
                            passenger_number_config=passenger_number_config)
    try:
        view.start_mainloop()
    except KeyboardInterrupt:
        logging.exception("something wrong to be logged")
        controller.close_on_escape()
    except Exception as e:
        logging.exception("something wrong to be logged")
        controller.close_on_escape()
