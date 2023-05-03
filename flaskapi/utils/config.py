import json
import os

CONF_FILE_NAME = "apis_conf"

def get_json_config():
    """Return a reference to the config file."""
    filepath = os.path.join(os.getenv("CONFROOT"), CONF_FILE_NAME + ".json")
    config = json.load(open(filepath))
    return config