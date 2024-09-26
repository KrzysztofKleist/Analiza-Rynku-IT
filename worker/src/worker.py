import os
import sys

# Get the current working directory
current_working_directory = os.getcwd()
log_utils = os.path.join(current_working_directory, "logs/utils")
sys.path.append("")

import json
from utils import get_website_data
from logs.utils import setup_logger

# Setup loggers
selenium_logger = setup_logger("selenium_logger", "logs/selenium.log")

# Get the worker settings.json
worker_settings_file = os.path.join(current_working_directory, "worker/settings.json")
# Load settings from JSON file
with open(worker_settings_file) as f:
    settings = json.load(f)
# Set values as environment variables
for key, value in settings.items():
    os.environ[key] = str(value)  # Convert value to string if it's not already


def main():
    url = os.getenv("URL")

    get_website_data(url, selenium_logger)

    selenium_logger.info("Program has exited")


if __name__ == "__main__":
    main()
