import asyncio
import websockets

from discord_lib2 import exception_catcher
from discord_lib2.logger import Logger
from discord_lib2.exception_catcher import ExceptionCatcher
from discord_lib2.event import GatewayEvent
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.Network.gateway.websocket import WebsocketController
from discord_lib2.Network.gateway.event_handler import EventHandler
from discord_lib2.Network.http_request.http import HttpRequestController
from discord_lib2.Network.http_request.request_loader import RequestLoader
from discord_lib2.terminal import Terminal
from discord_lib2.objects.http_request.body import b_gateway

class Runtime:
  def __init__(self, bot_token: str, bot_intents: int, os_type: str, logger_master: Logger, bootcycle: int, user_event: GatewayEvent):
    self.bootcycle = bootcycle
    self.logger = logger_master.get_child("RTM")

    self.system_cache_vault = SystemCacheVault()
    self.system_cache_vault.bot_token   = bot_token
    self.system_cache_vault.bot_intents = bot_intents
    self.system_cache_vault.os_type     = os_type

    self.exception_catcher = ExceptionCatcher(logger_master)
    self.http_request_loader = RequestLoader(logger_master)
    self.http_request_controller = HttpRequestController(self.system_cache_vault, logger_master)
    self.gateway_controller = WebsocketController(logger_master, self.system_cache_vault, self.exception_catcher)
    self.event_handler = EventHandler(logger_master, self.exception_catcher, self.system_cache_vault, self.gateway_controller, self.http_request_controller, user_event, self.http_request_loader)
    self.terminal_controller = Terminal(logger_master)

    # terminal commands
    self.terminal_command_functions = {
      "stop": self.__command_stop,
      "reconnect": self.__command_reconnect
    }

  async def boot(self):
    await self.terminal_controller.start()
    await self.http_request_controller.request_worker_start()
    await self.event_handler.start()
    self.logger.debug("get gateway url")


    get_gateway = self.http_request_loader.request_load(b_gateway.GetGateway())
    res = await self.http_request_controller.add_request(get_gateway)
    if res is None:
      self.logger.error("Failed load request payload | name: Get Gateway")
      return
    gateway_url = res.json().get("url")
    self.system_cache_vault.gateway.gateway_url = gateway_url

    while True:
      try:
        if self.bootcycle > 0:
          self.bootcycle -= 1
        self.logger.info(f"connection start | Remaining startup times: {self.bootcycle}")
        gw_res = await self.gateway_controller.websocket_connect()
        if not gw_res:
          self.logger.error("Failed connect gateway. system shutdown.")
          break
        
        while True:
          try:
            command = await self.terminal_controller.get_input()
            if command in self.terminal_command_functions:
              await self.terminal_command_functions[command]()
          except asyncio.QueueEmpty:
            pass

          await asyncio.to_thread(self.exception_catcher.get_v)
          await asyncio.sleep(1)

      except exception_catcher.StopConnection as e:
        await self.gateway_controller.websocket_disconnect(code=e.close_code, reason=e.close_reason)
        self.logger.info("safe close connection.")
        break

      except exception_catcher.ReConnection as e:
        await self.gateway_controller.websocket_disconnect(code=e.close_code, reason=e.close_reason)
        if self.bootcycle == 0:
          self.logger.info("remaining reconnection attempts is 0, system shutdown.")
          break
        self.logger.info("safe close connection, and reconnect.")

      except websockets.ConnectionClosedError:
        self.logger.error("The connection has been lost. try reconnect.")
        await self.gateway_controller.websocket_disconnect(code=0, reason="", only_task_stop=True)

      except Exception as e:
        await self.gateway_controller.websocket_disconnect(code=1000, reason="auto shutdown")
        self.logger.exception(f"application error | reason: {str(e)}")
        break
    
    await self.event_handler.stop()
    await self.http_request_controller.request_worker_stop()
    await self.terminal_controller.stop()
    await asyncio.sleep(1)
    await asyncio.to_thread(print, "application was shutdown. please pless Enter key...........")

#############################################################################
## User command functions
#############################################################################

#############################################################################
## Default command functions
#############################################################################
  async def __command_stop(self):
    self.exception_catcher.set_v(self.exception_catcher.STOP, 1000, "auto shutdown")

  async def __command_reconnect(self):
    self.exception_catcher.set_v(self.exception_catcher.RECONNECT, 4000, "auto reconnection")