import yaml
import logging
from datetime import datetime

def load_config(file_path):
    """
    Loads the configuration from a YAML file.
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

def log_message(message, log_file="data/logs/bot.log"):
    """
    Logs a message to a specified log file.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with open(log_file, "a") as file:
            file.write(log_entry)
    except Exception as e:
        print(f"Error logging message: {e}")
