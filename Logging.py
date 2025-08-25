import logging
import sys
from logging.handlers import RotatingFileHandler
from termcolor import colored
import functools

# Форматтер для цветного вывода в консоль
class ColoredConsoleFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red'
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname, 'white'))

# Настройка логгера
def setup_logger(log_file='app.log', console_level=logging.INFO, file_level=logging.DEBUG):
    app_logger = logging.getLogger('MyApp')
    app_logger.setLevel(logging.DEBUG)

    if not app_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_formatter = ColoredConsoleFormatter('%(asctime)s - %(name)s - %(levelname)s - <main_file> - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        app_logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - <main_file> - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        app_logger.addHandler(file_handler)

    return app_logger

def log_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('MyApp')
        logger.debug(f"Entering function {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting function {func.__name__} with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in function {func.__name__}: {e}")
            raise
    return wrapper