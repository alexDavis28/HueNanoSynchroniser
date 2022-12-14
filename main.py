import json
import config
from phue import Bridge
from rgbxy import Converter
from nanoleafapi import Nanoleaf
from os.path import exists

c = Converter()


def setup(config_file_path: str = "HNSConfig.json") -> (Nanoleaf, Bridge, dict):
    # Check config exists
    if not exists(config_file_path):
        config.create_config(config_file_path)

    # Load config and prompt for missing data
    config_data = config.load_config(config_file_path)

    for key in config_data:
        if config_data[key] is None:
            print(f"No value set for {key}")
            value = input(f"Enter value for {key}: ")
            config.update_config(config_file_path, key, value)
    config_data = config.load_config(config_file_path)

    nl = Nanoleaf(config_data["nanoleafIP"])
    b = Bridge(config_data["pHueHubIP"])
    return nl, b, config_data


def sync_lights(nanoleaf: Nanoleaf, bridge: Bridge, config_data: dict):
    xy = bridge.get_group(config_data["pHueGroup"], "xy")
    rgb = c.xy_to_rgb(*xy)
    nanoleaf.set_color(rgb)

    bri = bridge.get_group(config_data["pHueGroup"], "bri")
    bri_percent = (int((bri / 255) * 100)) if bri < 179 else 70  # Don't change the numbers!
    print(bri, bri_percent)
    nanoleaf.set_brightness(bri_percent, 1)


def sync_to_colour(nanoleaf: Nanoleaf, bridge: Bridge, config_data: dict, r: int = 0, g: int = 0, b: int = 0):
    xy = c.rgb_to_xy(r, g, b)
    bridge.set_group(config_data["pHueGroup"], "xy", xy)
    nanoleaf.set_color((r, g, b))


if __name__ == '__main__':
    nl, b, config_data = setup()
    sync_lights(nl, b, config_data)
