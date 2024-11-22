import json
import os

CONFIG_FILE = "/etc/tterminal/config.json"

def get_settings_button_timeout():
    """
    Načítanie aktuálneho timeoutu pre tlačidlo Settings.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        return config.get("settings_button_timeout", 3)
    return 3

def set_settings_button_timeout(timeout):
    """
    Uloženie timeoutu pre tlačidlo Settings.
    """
    if not os.path.exists(CONFIG_FILE):
        config = {}
    else:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

    config["settings_button_timeout"] = timeout

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
