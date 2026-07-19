import os
import logging
import queue
from logging.handlers import QueueHandler, QueueListener
from datetime import datetime

class Logger:
  LOG_DEFAULTFORMATTER = logging.Formatter("%(asctime)s[%(name)s][%(levelname)s] %(message)s")
  LOG_PARENT_NAME = "BotLib"

  def __init__(self):
    self.logger = logging.getLogger(self.LOG_PARENT_NAME)
    self.logger.setLevel(logging.DEBUG)

    self.logger.addHandler(logging.NullHandler())

    self.__listener = None
  
  def get_child(self, name: str):
    return logging.getLogger(f"{self.LOG_PARENT_NAME}.{name}")
  
  def create_default_handler(self, log_directory: str):
    if not os.path.exists(log_directory):
      os.makedirs(log_directory)

    log_path = os.path.join(log_directory, f'log{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    logger_handler_console = logging.StreamHandler()
    logger_handler_console.setLevel(logging.DEBUG)
    logger_handler_console.setFormatter(self.LOG_DEFAULTFORMATTER)

    logger_handler_file = logging.FileHandler(log_path, encoding="utf-8")
    logger_handler_file.setLevel(logging.INFO)
    logger_handler_file.setFormatter(self.LOG_DEFAULTFORMATTER)

    log_queue = queue.Queue()

    self.__listener = QueueListener(log_queue, logger_handler_console, logger_handler_file, respect_handler_level=True)
    self.__listener.start()

    async_handler = QueueHandler(log_queue)
    self.logger.addHandler(async_handler)

  def stop_default_handler(self):
    if self.__listener:
      self.__listener.stop()