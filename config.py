import json

def load_config(config_file_path) -> dict:
    with open(config_file_path, "r") as file:
        config_data = json.load(file)
    return config_data


def write_config(config_file_path, config_data):
    with open(config_file_path, "w") as file:
        json.dump(config_data, file)


def update_config(config_file_path, key, new_value):
    config_data = load_config(config_file_path)
    config_data[key] = new_value
    write_config(config_file_path, config_data)


def create_config(config_file_path):
    default_data = {
        "nanoleafIP": None,
        "pHueHubIP": None,
        "pHueGroup": None
    }
    open(config_file_path, "w+").close()
    write_config(config_file_path, default_data)