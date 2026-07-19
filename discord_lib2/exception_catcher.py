from typing import Literal
from discord_lib2.logger import Logger

class StopConnection(Exception):
  def __init__(self, close_code: int=1000, close_reason: str="auto shutdown") -> None:
    super().__init__(f"stop connection(exception used) | code: {close_code}, reason: {close_reason}")
    self.close_code = close_code
    self.close_reason = close_reason

class ReConnection(Exception):
  def __init__(self, close_code: int=4000, close_reason: str="auto reconnection") -> None:
    super().__init__(f'reconnection(exception used) | code: {close_code}, reason: {close_reason}')
    self.close_code = close_code
    self.close_reason = close_reason

class ExceptionCatcher:
  RECONNECT = "reconnect"
  STOP = "stop"
  def __init__(self, logger: Logger) -> None:
    self.logger = logger.get_child("EXC")
    self.name: str
    self.close_code: int
    self.close_reason: str
    self.flag = False
    self.exception_function = {
      self.RECONNECT: self.__reconnect,
      self.STOP:      self.__stop
    }
  
  def set_v(self, name: Literal["stop", "reconnect"], close_code: int, close_reason: str):
    self.name = name
    self.close_code = close_code
    self.close_reason = close_reason
    self.logger.debug(f"Catched exception | code: {close_code}, reason: {self.close_reason}")
    self.flag = True

  def get_v(self):
    if self.flag:
      raise self.exception_function[self.name]()

  def __stop(self):
    self.flag = False
    raise StopConnection(self.close_code, self.close_reason)
  
  def __reconnect(self):
    self.flag = self.flag
    raise ReConnection(self.close_code, self.close_reason)