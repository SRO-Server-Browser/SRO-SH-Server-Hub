# src/core/logger.py
from utils.colors import Loader, print_success, print_fail, print_debug, print_warning, box, color
import logging
import os

class Logger:
    def __init__(self, log_file="logs/server_hub.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def success(self, message):
        print_success(message)
        logging.info(message)

    def fail(self, message):
        print_fail(message)
        logging.error(message)

    def debug(self, message):
        print_debug(message)
        logging.debug(message)

    def warning(self, message):
        print_warning(message)
        logging.warning(message)

    def box(self, *args, color_code=color.Blue):
        box.print(*args, color_code=color_code)
    
    def log(self, *args):
        logging.debug(message)
        self.info(message) # for test purpose normally I need to log a file