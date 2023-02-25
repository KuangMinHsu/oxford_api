import os
import logging
import logging.handlers

LOG_DIR = "/var/log/oxford-api/"

LEVEL = logging.DEBUG


def set_logger():
    general_formatter = logging.Formatter(
        '%(asctime)-15s -%(module)-8s- '
        '%(lineno)-4d [%(levelname)s] %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(LEVEL)
    console.setFormatter(general_formatter)

    general_file_log = logging.handlers.RotatingFileHandler(
        os.path.join(LOG_DIR, "general"),
        maxBytes=1024 * 1024 * 5, backupCount=5
    )
    general_file_log.setLevel(LEVEL)
    general_file_log.setFormatter(general_formatter)
    general_logger = logging.getLogger("general")
    general_logger.propagate = False
    general_logger.addHandler(general_file_log)
    general_logger.setLevel(logging.DEBUG)
