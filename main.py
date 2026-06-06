from controller.main import Controller
from view.main import View
from config.config_reader import read_config
from datetime import datetime


config = read_config()
db_name_config = config["database"]["name"]
trip_purposes_config: list = config["database"]["trip_purposes"]
list_captain_config: list = config["database"]["captain_config"]
if db_name_config == "telemetry.db":
    db_name_config = datetime.now().strftime("%Y_%m_%d_") + db_name_config
server_ip_config = config["cerbo_gx"]["server_ip"]
passenger_number_config: dict = config["passenger_number"]
communities_config: dict = config["communities_config"]
biodiversity_config: list = config["database"]["biodiversity_config"]
biodiversity_number_config: dict = config["biodiversity_number"]


if __name__ == "__main__":
    # TODO: create the logging hierarchy and pass it to the modules.
    view = View(passenger_number_config, trip_purposes_config=trip_purposes_config,
                list_captain_config=list_captain_config, communities_config=communities_config,
                biodiversity_config=biodiversity_config,
                biodiversity_number_config=biodiversity_number_config)
    controller = Controller(view=view, db_name=f"model/{db_name_config}",
                            server_ip_config=server_ip_config,
                            passenger_number_config=passenger_number_config,
                            trip_purposes_config=trip_purposes_config,
                            captain_config=list_captain_config,
                            communities_config=communities_config)
    try:
        view.start_mainloop()
    except KeyboardInterrupt:
        controller.close_on_escape()
    except Exception as e:
        controller.close_on_escape()
