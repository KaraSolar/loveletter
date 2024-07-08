from controller.main import Controller
from view.main import View
from config.config_reader import read_config

config = read_config()
db_name_config = config["database"]["name"]
server_ip_config = config["cerbo_gx"]["server_ip"]
passenger_number_config: dict = config["passenger_number"]



if __name__ == "__main__":
    # TODO: create the logging hierarchy and pass it to the modules.
    view = View(passenger_number_config)
    controller = Controller(view=view, db_name=f"model/{db_name_config}",
                            server_ip_config=server_ip_config,
                            passenger_number_config=passenger_number_config)
    try:
        view.start_mainloop()
    except KeyboardInterrupt:
        controller.close_on_escape()
    except Exception as e:
        controller.close_on_escape()
