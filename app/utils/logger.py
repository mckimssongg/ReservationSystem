import os
import logging
from functools import wraps

class LoggerConfig:
    def __init__(self, file_name: str, log_folder: str = "logs"):
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
            
        file_path = os.path.join(log_folder, file_name + ".log")
        
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s-%(levelname)s:%(message)s')
        
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_message(self, message: str, level: str):
        level = level.lower()
        message = message.lower()
        
        if level not in ["info", "warning", "error"]:
            raise ValueError("Invalid level")
        
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)

def log_decorator(logger, level="info"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            log_message = f"Call to '{func.__name__}' > {result}"
            logger.log_message(log_message, level)
            return result
        return wrapper
    return decorator
