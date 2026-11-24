import asyncio
from logging import Logger
from typing import Callable, Any, Awaitable

from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.network.gateway.websocket import WebsocketController, DispatchEventData

class EventDispatcher:
  cache_functions: dict[str, Callable[[dict], Awaitable[None]]] = {}
  lib_task_functions: dict[str, Callable] = {}
  user_event_functions: dict[str, Callable] = {}
  task_worker = None

  def __init__(self, logger: Logger, exception_catcher: ExceptionCatcher2, gateway_controller: WebsocketController) -> None:
    self.logger = logger
    self.exception_catcher = exception_catcher
    self.gateway_controller = gateway_controller

  def regist_cache_functions(self, functions: dict[str, Callable]):
    for k, f in functions.items():
      self.cache_functions[k] = f

  def regist_user_event_functions(self, functions: dict[str, Callable]):
    for k, f in functions.items():
      self.user_event_functions[k] = f

  def regist_lib_task_functions(self, functions: dict[str, Callable]):
    for k, f in functions.items():
      self.lib_task_functions[k] = f

  async def __dispatch_worker(self):
    self.logger.info("Task started | name: worker=handler.dispatch_worker")
    try:
      while True:
        dispatch_data: DispatchEventData = await self.gateway_controller.get_event_queue()
        await self.__event_trigger(dispatch_data)
    except asyncio.CancelledError:
      return
    #TODO 仮 - 例外取得
    except Exception as e:
      self.logger.exception(f"dispatch worker error | reason: {str(e)}")

  async def __event_trigger(self, event_data: DispatchEventData):
    await self.__run_task(event_data.data, event_data.name, self.cache_functions, "cache_update", True)
    await self.__run_task(event_data.data, event_data.name, self.lib_task_functions, "task")
    await self.__run_task(event_data.data, event_data.name, self.user_event_functions, "user_event", True)

  async def __run_task(self, event_data: dict[str, Any], event_name: str, function_dict: dict[str, Callable], log_task_name: str, unknown_error: bool=False):
    if event_name in function_dict:
      try:
        await function_dict[event_name](event_data)
      except Exception as e:
        self.logger.exception(f"event execution error | task: {log_task_name} | reason: {str(e)}")
    elif unknown_error:
      self.logger.error(f"unknown event | task: {log_task_name} | event: {event_name}")

  async def start(self):
    self.task_worker = asyncio.create_task(self.__dispatch_worker())

  async def stop(self):
    if self.task_worker:
      try:
        self.task_worker.cancel()
        await self.task_worker
      except:
        pass
      finally:
        self.logger.info(f"Task stopped | worker=handler.dispatch_worker")