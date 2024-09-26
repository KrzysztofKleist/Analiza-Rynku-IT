import os
import logging


def setup_logger(name, log_file, level=logging.INFO):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Get the current working directory
    current_working_directory = os.getcwd()
    log_file = os.path.join(current_working_directory, log_file)
    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(log_file):
        # Create the file
        with open(log_file, "w") as file:
            file.write("")  # Create an empty file

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Set level for handlers to INFO and above
    file_handler.setLevel(logging.INFO)  # Log INFO and higher levels to the file
    console_handler.setLevel(
        logging.INFO
    )  # Print INFO and higher levels to the console

    # Create formatters and add them to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log a message to check if file handler works
    logger.info(f"Logger {name} initialized successfully")

    return logger
