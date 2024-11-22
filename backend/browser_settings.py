import json
import os

CONFIG_FILE = "/etc/tterminal/config.json"

def get_browser_url():
    """
    Načítanie aktuálnej URL adresy z konfigurácie.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        return config.get("browser_url", "")
    return ""

def set_browser_url(url):
    """
    Uloženie URL adresy do konfigurácie.
    """
    if not os.path.exists(CONFIG_FILE):
        config = {}
    else:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

    config["browser_url"] = url

    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

