from logging import Logger
from typing import Callable
import asyncio
from aioconsole import ainput

from discord_lib2.logger import Logger as MLogger
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2
from discord_lib2.command.terminal_command import TerminalCommand
from discord_lib2.objects.resources import UserTerminalCommandResources
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.cache.user.data import DataCacheVault

##########################################################################

class TerminalListener:
  input_queue: asyncio.Queue
  def __init__(self, logger: Logger) -> None:
    self.input_queue = asyncio.Queue()
    self.logger = logger

  async def __worker_terminal_listener(self):
    self.logger.info("Task started | name: worker=terminal_listener")
    try:
      while True:
        inputted_command = await ainput("")
        inputted_command = inputted_command.strip()
        self.logger.info(f"input | {inputted_command}")
        await self.input_queue.put(inputted_command)
        await asyncio.sleep(0.1)
    except EOFError:
      return
    except asyncio.CancelledError:
      return
    except Exception as e:
      self.logger.exception(f"worker error | reason: {str(e)}")

  async def start(self):
    self.__task__terminal_listener = asyncio.create_task(self.__worker_terminal_listener())

  async def stop(self):
    if self.__task__terminal_listener:
      self.__task__terminal_listener.cancel()
      try:
        await self.__task__terminal_listener
      except:
        pass
      finally:
        self.logger.info("Task stopped | name: worker=terminal_listener")

  def get_input(self):
    inputted_command: str = self.input_queue.get_nowait()
    self.input_queue.task_done()
    return inputted_command.split(" ")

##########################################################################

class TerminalRT:
  def __init__(self, logger: MLogger, exception_catcher: ExceptionCatcher2, utcs: TerminalCommand) -> None:
    self.logger = logger.get_child("Terminal")
    self.terminal_listener = TerminalListener(self.logger)
    self.exception_catcher = exception_catcher
    self.utcs = utcs          # uesr terminal commands

    # default terminal commands
    self.dtc_funcs: dict[str, Callable] = {
      "stop": self.dtc_stop,
      "reconnect": self.dtc_reconnect,
      "list": self.dtc_list
    }
  
  async def start(self) -> None:
    await self.terminal_listener.start()

  async def stop(self) -> None:
    await self.terminal_listener.stop()

  def gen_resources(self, gr: GatewayRequest, hr: HttpRequest, dc: DataCacheVault) -> None:
    self.utcr = UserTerminalCommandResources(gr, hr, dc, self.logger, self.exception_catcher)

  async def tc_execution(self) -> None:
    try:
      command = self.terminal_listener.get_input()
    except asyncio.QueueEmpty:
      return
    command_name = command[0]
    if command_name == "":
      return
    try:
      if command_name in self.dtc_funcs:
        await self.dtc_funcs[command_name](command)
      elif command_name in self.utcs.user_command_functions:
        await self.utcs.user_command_functions[command_name](command, self.utcr)
      else:
        self.logger.error(f"unknown command: \"{command_name}\"")
    except Exception as e:
      self.logger.exception(f"Command execution error | reason: {str(e)}")

  async def dtc_stop(self, args: list[str]):
    await self.exception_catcher.set_v(self.exception_catcher.STOP, 1000, "user shutdown")

  async def dtc_reconnect(self, args: list[str]):
    await self.exception_catcher.set_v(self.exception_catcher.RECONNECT, 4000, "user reconnection")

  async def dtc_list(self, args: list[str]):
    self.logger.info("==================")
    self.logger.info("<< COMMAND LIST >>")
    self.logger.info("Default Commands")
    for command_name in self.dtc_funcs.keys():
      self.logger.info(f"- {command_name}")
    self.logger.info("User Commands")
    for command_name in self.utcs.user_command_functions.keys():
      self.logger.info(f"- {command_name}")
    self.logger.info("==================")