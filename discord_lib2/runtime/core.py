from dacite import from_dict
import asyncio

from discord_lib2.logger import Logger
from discord_lib2.event import GatewayEvent
from discord_lib2.command.terminal_command import TerminalCommand
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.Network.http_request.http import HttpRequestController
from discord_lib2.Network.http_request.request_loader import RequestLoader
from discord_lib2.Network.http_request.http import RequestFailedError
from discord_lib2.Network.gateway.websocket import WebsocketController
from discord_lib2.Network.gateway.event_handler import EventHandler

from discord_lib2.runtime.terminal import TerminalRT
from discord_lib2.runtime.appcom_check import update_global_appcom
from discord_lib2.runtime.exception_catcher import ExceptionCatcher2, StopConnection, ReConnection, ReStartConnection

from discord_lib2.objects.gateway import recv_event_object

from discord_lib2.objects.http_request.body import b_application
from discord_lib2.objects.http_request.body import b_gateway

class StopGatewayConnectionError(Exception):
  def __init__(self, can_reconnect: bool=True, message: str="") -> None:
    super().__init__(f"stop gateway connection | can_reconnect: {can_reconnect}, message: {message}")
    self.can_reconnect = can_reconnect
    self.message = message

class FailedGatewayConnectionError(Exception):
  def __init__(self, message: str) -> None:
    super().__init__(f"failed gateway connection | message: {message}")
    self.message = message

class FailedGetCurrentApplicationError(Exception):
  def __init__(self, reason) -> None:
    super().__init__(reason)
    self.reason = str(reason)

class FailedGetGatewayError(Exception):
  def __init__(self, reason) -> None:
    super().__init__(reason)
    self.reason = str(reason)

class Runtime:
  def __init__(
      self,
      bot_token: str,
      bot_intents: int,
      os_type: str,
      logger_master: Logger,
      bootcycle: int,
      user_event: GatewayEvent,
      user_terminal_command: TerminalCommand,
      application_commands: dict,
      proxy: str | None
  ):
    self.bootcycle = bootcycle
    self.logger = logger_master.get_child("Runtime")

    self.system_cache_vault = SystemCacheVault()
    self.data_cache_vault = DataCacheVault()
    self.system_cache_vault.bot_token   = bot_token
    self.system_cache_vault.bot_intents = bot_intents
    self.system_cache_vault.os_type     = os_type
    self.system_cache_vault.proxy       = proxy

    self.exception_catcher = ExceptionCatcher2(logger_master)
    self.terminal_controller = TerminalRT(
      logger_master,
      self.exception_catcher,
      user_terminal_command
    )
    self.httpapi_request_loader = RequestLoader(logger_master)
    self.httpapi_request_controller = HttpRequestController(
      self.system_cache_vault,
      logger_master
    )
    self.gateway_controller = WebsocketController(
      logger_master,
      self.system_cache_vault,
      self.exception_catcher
    )
    self.event_handler = EventHandler(
      logger_master,
      self.exception_catcher,
      self.system_cache_vault,
      self.data_cache_vault,
      self.gateway_controller,
      self.httpapi_request_controller,
      user_event,
      self.httpapi_request_loader,
      application_commands
    )

    self.terminal_controller.gen_resources(
      GatewayRequest(self.gateway_controller),
      HttpRequest(self.httpapi_request_controller,
      self.httpapi_request_loader),
      self.data_cache_vault
    )

    self.application_commands = application_commands

  async def __start_base_workers(self):
    await self.terminal_controller.start()
    await self.httpapi_request_controller.request_worker_start()
    await self.event_handler.start()

  async def __stop_base_workers(self):
    await self.event_handler.stop()
    await self.httpapi_request_controller.request_worker_stop()
    await self.terminal_controller.stop()

  async def __get_current_application(self) -> recv_event_object.Application:
    self.logger.info("get current applicatoin")
    req_data = self.httpapi_request_loader.load_request(b_application.GetCurrentApplication())
    try:
      res = await self.httpapi_request_controller.add_request(req_data)
    except RequestFailedError as e:
      raise FailedGetCurrentApplicationError(e.name)
    if not res.ok:
      raise FailedGetCurrentApplicationError(res.json)
    return from_dict(recv_event_object.Application, res.json)

  async def __get_gateway_url(self) -> str:
    self.logger.info("get gateway url")
    req_data = self.httpapi_request_loader.load_request(b_gateway.GetGateway())
    try:
      res = await self.httpapi_request_controller.add_request(req_data)
    except RequestFailedError as e:
      raise FailedGetGatewayError(e.name)
    if not res.ok:
      raise FailedGetGatewayError(res.json)
    gateway_url = res.json.get("url")
    if gateway_url is None:
      raise FailedGetGatewayError("url payload is None")
    return gateway_url

  async def __session(self):
    await self.exception_catcher.reset_queue()
    gw_con_st = await self.gateway_controller.websocket_connect()
    if not gw_con_st:
      raise FailedGatewayConnectionError("failed connection")
    try:
      while True:
        await self.terminal_controller.tc_execution()
        self.exception_catcher.get_v()
        await asyncio.sleep(0.1)
    except StopConnection as e:
      await self.gateway_controller.websocket_disconnect(code=e.close_code, reason=e.close_reason)
      raise StopGatewayConnectionError(False, "system shutdown")
    except ReConnection as e:
      if self.bootcycle == 0:
        await self.gateway_controller.websocket_disconnect(code=1000, reason="auto shutdown")
        raise StopGatewayConnectionError(False, "remaining reconnection attempts is 0, system shtdown")
      else:
        await self.gateway_controller.websocket_disconnect(code=e.close_code, reason=e.close_reason)
        raise StopGatewayConnectionError(True, "system reconnection")
    except ReStartConnection as e:
      await self.gateway_controller.websocket_disconnect(code=e.close_code, reason=e.close_reason)
      if self.bootcycle == 0:
        raise StopGatewayConnectionError(False, "remaining reconnection attempts is 0, system shtdown")
      else:
        self.system_cache_vault.resume.reconnect_gateway_url = ""
        self.system_cache_vault.resume.session_id = ""
        raise StopGatewayConnectionError(True, "system reconnection")
    except asyncio.CancelledError:
      await self.gateway_controller.websocket_disconnect(code=1000, reason="auto shutdown")
      raise
    except Exception as e:
      await self.gateway_controller.websocket_disconnect(code=1000, reason="auto shutdown")
      raise

  async def __connection_loop(self):
    wait_time = 1
    wait_count = 0
    while True:
      try:
        if self.bootcycle == 0:
          self.logger.info("remaining reconnection attempts is 0, system shutdown.")
          break
        if self.bootcycle > 0:
          self.bootcycle -= 1
        self.logger.info(f"remaining reconnection attempts: {self.bootcycle}")
        await self.__session()
      except StopGatewayConnectionError as e:
        self.logger.info(f"stopped gateway connection | message: {e.message}, reconnect: {e.can_reconnect}")
        wait_time = 1
        wait_count = 0
        if not e.can_reconnect:
          break
      except FailedGatewayConnectionError as e:
        if wait_count >= 10:
          self.logger.error(f"gateway connection failed count: 10, system shutdown")
          break
        wait_count += 1
        self.logger.info(f"waiting... ({wait_time}s)")
        await asyncio.sleep(wait_time)
        wait_time *= 2
      except asyncio.CancelledError:
        raise
      except Exception as e:
        self.logger.exception(f"application error, system shutdown | reason: {str(e)}")
        break

  async def boot(self):
    await self.__start_base_workers()

    try:
      self.data_cache_vault.data.application = await self.__get_current_application()
    except FailedGetCurrentApplicationError as e:
      self.logger.error(f"failed get current application | reason: {e}")
      await self.__stop_base_workers()
      return

    try:
      self.system_cache_vault.gateway.gateway_url = await self.__get_gateway_url()
    except FailedGetGatewayError as e:
      self.logger.error(f"failed get gateway url | reason: {e}")
      await self.__stop_base_workers()
      return

    await update_global_appcom(
      self.logger,
      self.httpapi_request_loader,
      self.httpapi_request_controller,
      self.data_cache_vault,
      self.application_commands["globals"]
    )

    loop_task = asyncio.create_task(self.__connection_loop())
    try:
      await loop_task
    except asyncio.CancelledError:
      self.logger.info("inputted SIGINT")
      try:
        loop_task.cancel()
        await loop_task
      except:
        pass
    await self.gateway_controller.session_close()

    await self.__stop_base_workers()
    self.logger.info("system shutdowned")