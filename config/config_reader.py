import yaml


def read_config(filename="config/config.yml"):
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)


def telemetry_configuration(config: yaml.safe_load) -> dict:
    target = config["telemetry"]["target"]
    if target == "cerbo_gx":
        return {"target": target, "config": config["telemetry"]["cerbo_gx"]["server_ip"]}
    if target == "canbus":
        return {"target": target, "config": config["telemetry"]["canbus"]["channel"]}
    else:
        raise ValueError("Not a valid input")