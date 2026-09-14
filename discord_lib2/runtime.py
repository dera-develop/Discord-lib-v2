import asyncio
import websockets
from dacite import from_dict

from discord_lib2 import exception_catcher
from discord_lib2.logger import Logger
from discord_lib2.exception_catcher import ExceptionCatcher
from discord_lib2.event import GatewayEvent
from discord_lib2.cache.system.system import SystemCacheVault
from discord_lib2.cache.user.data import DataCacheVault
from discord_lib2.Network.gateway.websocket import WebsocketController
from discord_lib2.Network.gateway.event_handler import EventHandler
from discord_lib2.Network.http_request.http2 import HttpRequestController, RequestFailedError
from discord_lib2.Network.http_request.request_loader import RequestLoader
from discord_lib2.terminal import Terminal
from discord_lib2.command.terminal_command import TerminalCommand 
from discord_lib2.objects.resources import UserTerminalCommandResources
from discord_lib2.objects.gateway import recv_event_object
from discord_lib2.objects.gateway.user_request import GatewayRequest
from discord_lib2.objects.gateway import recv_event_object
from discord_lib2.objects.http_request.user_request import HttpRequest
from discord_lib2.command.appcom_diffchecker import checker_v2

from discord_lib2.objects.http_request.body import b_gateway
from discord_lib2.objects.http_request.body import b_application
from discord_lib2.objects.http_request.body import b_application_command
from discord_lib2.objects.http_request.request_query import q_application_command

class SkipTaskException(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

class Runtime:
  def __init__(self, bot_token: str, bot_intents: int, os_type: str, logger_master: Logger, bootcycle: int, user_event: GatewayEvent, user_terminal_command: TerminalCommand, application_commands: dict):
    self.bootcycle = bootcycle
    self.logger = logger_master.get_child("RTM")

    self.system_cache_vault = SystemCacheVault()
    self.data_cache_vault = DataCacheVault()
    self.system_cache_vault.bot_token   = bot_token
    self.system_cache_vault.bot_intents = bot_intents
    self.system_cache_vault.os_type     = os_type
    self.application_commands = application_commands

    self.exception_catcher = ExceptionCatcher(logger_master)
    self.http_request_loader = RequestLoader(logger_master)
    self.http_request_controller = HttpRequestController(self.system_cache_vault, logger_master)
    self.gateway_controller = WebsocketController(logger_master, self.system_cache_vault, self.exception_catcher)
    self.event_handler = EventHandler(logger_master, self.exception_catcher, self.system_cache_vault, self.data_cache_vault, self.gateway_controller, self.http_request_controller, user_event, self.http_request_loader, application_commands)
    self.terminal_controller = Terminal(logger_master)

    # terminal commands
    self.terminal_command_functions = {
      "stop": self.__command_stop,
      "reconnect": self.__command_reconnect,
      "list": self.__command_list
    }

    self.user_terminal_command = user_terminal_command
    self.user_terminal_command_resources = UserTerminalCommandResources(
      GatewayRequest(self.gateway_controller),
      HttpRequest(self.http_request_controller, self.http_request_loader),
      self.data_cache_vault,
      logger_master
    )


  async def __regist_application_command(self):
    self.logger.info("checking command difference...")
    # difference check
    ## global
    self.logger.debug("target: global_application_command")
    command_datas = self.application_commands["globals"]
    global_appcom_datas = []
    req_data = self.http_request_loader.request_load(
      b_application_command.GetGlobalApplicationCommands(),
      q_application_command.GetGlobalApplicationCommands(with_localizations=True),
      application_id=self.system_cache_vault.application.id
    )
    try:
      res = await self.http_request_controller.add_request(req_data)
      global_appcom_datas = checker_v2(res.json, command_datas)
    except RequestFailedError:
      self.logger.error("Failed request \"GetGlobalApplicationCommand\"")
    except:
      raise

    self.logger.info("application command updating...")

    # create, edit, delet
    ## global
    log_datas = {"new": 0, "edit": 0, "delete": 0}
    for data in global_appcom_datas:
      if data.get("new"):
        req_dict = data.get("data")
        req_data = self.http_request_loader.request_load(b_application_command.CreateGlobalApplicationCommand(req_dict), application_id=self.system_cache_vault.application.id)
        try:
          res = await self.http_request_controller.add_request(req_data)
          if res.ok:
            log_datas["new"] += 1
        except RequestFailedError:
          self.logger.error("Failed request \"CreateGlobalApplicationCommand\"")
      elif data.get("edit"):
        req_dict = data.get("data")
        req_com_id = data.get("id")
        req_data = self.http_request_loader.request_load(b_application_command.EditGlobalApplicationCommand(req_dict), application_id=self.system_cache_vault.application.id, command_id=req_com_id)
        try:
          res = await self.http_request_controller.add_request(req_data)
          if res.ok:
            log_datas["edit"] += 1
        except RequestFailedError:
          self.logger.error("Failed request \"EditGlobalApplicationCommand\"")
      elif data.get("del"):
        req_com_id = data.get("id")
        req_data = self.http_request_loader.request_load(b_application_command.DeleteGlobalApplicationCommand(), application_id=self.system_cache_vault.application.id, command_id=req_com_id)
        try:
          res = await self.http_request_controller.add_request(req_data)
          if res is not None and res.ok:
            log_datas["delete"] += 1
        except RequestFailedError:
          self.logger.error("Failed request \"DeleteGlobalApplicationCommand\"")
    self.logger.info(f"global command update | new: {log_datas['new']}, edit: {log_datas['edit']}, delete: {log_datas['delete']}")


  async def boot(self):
    await self.terminal_controller.start()
    await self.http_request_controller.request_worker_start()

    await asyncio.sleep(1)

    # get current application
    self.logger.debug("get current application")
    req_data = self.http_request_loader.request_load(b_application.GetCurrentApplication())
    res = None
    try:
      res = await self.http_request_controller.add_request(req_data)
    except RequestFailedError:
      pass
    if res is None or not res.ok:
      self.logger.error("Failed request | \"GetCurrentApplication\"")
      await self.http_request_controller.request_worker_stop()
      await self.terminal_controller.stop()
      await asyncio.sleep(1)
      await asyncio.to_thread(print, "application was shutdown. please pless Enter key...........")
      return

    self.system_cache_vault.application = from_dict(recv_event_object.Application, res.json)

    self.logger.info("check application command")
    try:
      await self.__regist_application_command()
    except:
      self.logger.exception("application command checker failed")
    self.logger.info("completed check application command")

    await self.event_handler.start()
    self.logger.debug("get gateway url")
    get_gateway = self.http_request_loader.request_load(b_gateway.GetGateway())
    try:
      res = await self.http_request_controller.add_request(get_gateway)
    except RequestFailedError:
      self.logger.error("Failed request \"GetGateway\"")
      await self.http_request_controller.request_worker_stop()
      await self.terminal_controller.stop()
      await asyncio.sleep(1)
      await asyncio.to_thread(print, "application was shutdown. please pless Enter key...........")
      return

    gateway_url = res.json.get("url")
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
            command_name = command[0]
            if command_name in self.terminal_command_functions:
              await self.terminal_command_functions[command_name](command)
            elif command_name in self.user_terminal_command.user_command_functions:
              await self.user_terminal_command.user_command_functions[command_name](command, self.user_terminal_command_resources)
            else:
              self.logger.warning(f"Command \"{command_name}\" not found")
          except asyncio.QueueEmpty:
            pass
          except Exception as e:
            self.logger.error(f"Command execution error | reason: {str(e)}")

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
    await asyncio.sleep(0.1)
    await asyncio.to_thread(print, "application was shutdown. please pless Enter key...........")

#############################################################################
## Default command functions
#############################################################################
  async def __command_stop(self, args: list[str]):
    self.exception_catcher.set_v(self.exception_catcher.STOP, 1000, "auto shutdown")


  async def __command_reconnect(self, args: list[str]):
    self.exception_catcher.set_v(self.exception_catcher.RECONNECT, 4000, "auto reconnection")


  async def __command_list(self, args: list[str]):
    self.logger.debug("==================")
    self.logger.debug("<< COMMAND LIST >>")
    self.logger.debug("Default Commands")
    for command_name in self.terminal_command_functions.keys():
      self.logger.debug(f"- {command_name}")
    self.logger.debug("User Commands")
    for command_name in self.user_terminal_command.user_command_functions.keys():
      self.logger.debug(f"- {command_name}")
    self.logger.debug("==================")