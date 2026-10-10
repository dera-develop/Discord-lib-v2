from typing import ClassVar
import asyncio

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

class ReStartConnection(Exception):
  def __init__(self, close_code: int=1000, close_reason: str="auto shutdown") -> None:
    super().__init__(f"restart connection(exception used) | code: {close_code}, reason: {close_reason}")
    self.close_code = close_code
    self.close_reason = close_reason

class ExceptionInformation:
  def __init__(self, name: str, code: int, reason: str) -> None:
    self.name = name
    self.close_code = code
    self.reason = reason

class ExceptionCatcher2:
  RECONNECT: ClassVar[str] = "reconnect"
  STOP: ClassVar[str] = "stop"
  RESTART: ClassVar[str] = "restart"

  def __init__(self, logger: Logger) -> None:
    self.logger = logger.get_child("EXC")
    self.exception_queue: asyncio.Queue[ExceptionInformation] = asyncio.Queue()
    self.exception_funcs = {
      self.RECONNECT: self.__reconnect_exception,
      self.STOP     : self.__stop_exception,
      self.RESTART  : self.__restart_exception
    }

  async def reset_queue(self):
    while not self.exception_queue.empty():
      self.exception_queue.get_nowait()

  async def set_v(self, name: str, close_code: int, close_reason: str):
    data = ExceptionInformation(name, close_code, close_reason)
    await self.exception_queue.put(data)

  def get_v(self):
    try:
      data = self.exception_queue.get_nowait()
    except asyncio.QueueEmpty:
      return
    self.logger.warning(f"catched exception | code: {data.close_code}, reason: {data.reason}")
    self.exception_funcs[data.name](data.close_code)

  def __stop_exception(self, close_code: int):
    raise StopConnection(close_code=close_code)

  def __reconnect_exception(self, close_code: int):
    raise ReConnection(close_code)

  def __restart_exception(self, close_code: int):
    raise ReStartConnection(close_code)