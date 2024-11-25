import logging
import os


def load_logger():
    log_file_path = "logs/" + "bot.log"
    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(log_file_path, 'w') as log_file:
        log_file.write('Logger started.')

    logging.basicConfig(filename="logs/bot.log", level=logging.INFO)

